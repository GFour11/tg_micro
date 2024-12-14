from typing import Union

import asyncio
import pickle
import logging
import queue
import socket
import sys
import threading
import setproctitle
import traceback
import struct
from abc import ABC, abstractmethod
from asyncio import StreamWriter, StreamReader
from typing import Any, TypeVar, Callable
from aioprocessing import AioQueue, AioProcess

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def get_logger():
    return logger


def debug(msg: str):
    get_logger().debug(msg)


def info(msg: str):
    get_logger().info(msg)


def warning(msg: str):
    get_logger().warning(msg)


def error(msg: str):
    get_logger().error(msg)


def critical(msg: str):
    get_logger().critical(msg)


BaseServerType = TypeVar('BaseServerType', bound='BaseServer')


class WorkerResult(int):
    pass


class AbstractClientHandler(ABC):
    def __init__(
            self,
            reader: StreamReader,
            writer: StreamWriter,
            server: BaseServerType
    ):
        self.reader = reader
        self.writer = writer
        self.server = server
        self.closed = False

    async def send_msg(self, msg: Any):
        if self.closed:
            raise ConnectionError("Connection closed")
        try:
            encoded = pickle.dumps(msg)
            self.writer.write(struct.pack('>I', len(encoded)))
            self.writer.write(encoded)
            await self.writer.drain()
        except ConnectionResetError as e:
            debug(f"ConnectionResetError: {e}")
            self.closed = True
            # await self.close()
        except BrokenPipeError as e:
            debug(f"BrokenPipeError: {e}")
            self.closed = True

    async def recv_msg(self):
        if self.closed:
            raise ConnectionError("Connection closed")
        try:
            raw_msg_len = await self.reader.readexactly(4)
            # noinspection PyTypeChecker
            msg_len = struct.unpack('>I', raw_msg_len)[0]
            data = await self.reader.readexactly(msg_len)
        except asyncio.exceptions.IncompleteReadError:
            return None
        if not data:
            return None

        # noinspection PyTypeChecker
        return pickle.loads(data)

    async def close(self):
        if self.closed:
            raise ConnectionError("Connection closed")
        try:
            self.writer.close()
            await self.writer.wait_closed()
        except BrokenPipeError:
            pass

    def get_server(self) -> BaseServerType:
        return self.server

    @abstractmethod
    async def handle(self):
        pass

    async def do_forwarding(
            self,
            worker_key: str,
            forward_result: bool = True,
            stop_on_none: bool = False
    ) -> Union[WorkerResult, None]:
        worker = self.get_server().get_worker(worker_key)
        if worker is None:
            raise ValueError(f"Worker with name {worker_key} not found")
        while True:
            message = await worker.read()
            debug(f"Received from worker {worker.get_key()}: {message} {type(message)}")
            if message is None and stop_on_none:
                return None
            if isinstance(message, WorkerResult):
                debug("!!! Terminating connection, result: " + str(message))
                if forward_result:
                    await self.send_msg(("r", message))
                return message
            await self.send_msg(("s", message))
            if not self.is_alive():
                return None

    def is_alive(self):
        return not self.closed


class StreamToMethod:
    def __init__(self, method):
        self.method = method

    def write(self, message):
        # message = message.strip()
        # if message:
        #     self.method(message)
        self.method(message[:-1] if message.endswith("\n") else message)

    def flush(self):
        pass


class AsyncStreamToMethod:
    def __init__(self, method):
        self.method = method
        self.loop = asyncio.get_event_loop()

    def write(self, message):
        message = message.strip()
        if message:
            # await self.method(message)
            self.loop.create_task(self.method(message))
            # task = self.loop.create_task(self.method(message))
            # await task
            # self.loop.create_task(self.ensure_task_completion(task))

    # async def ensure_task_completion(self, task):
    #     try:
    #         await task
    #     except asyncio.CancelledError:
    #         print("Task was cancelled")

    def flush(self):
        pass


class AbstractWorker(ABC):
    FORWARD_STDOUT = True
    FORWARD_STDERR = True

    def __init__(self, args: dict, queue_worker2server: AioQueue, queue_server2worker: AioQueue):
        self.args = args
        self.queue_worker2server = queue_worker2server
        self.queue_server2worker = queue_server2worker
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.stream_to_method_converter = StreamToMethod

    def get_args(self):
        return self.args

    @abstractmethod
    def queue_put(self, data):
        pass

    @abstractmethod
    def queue_get(self):
        pass

    def replace_stdout_stderr(self):
        if self.FORWARD_STDOUT:
            sys.stdout = self.stream_to_method_converter(lambda m: self.queue_put(m))
            change_loggers_stream(self.original_stdout, sys.stdout)

        if self.FORWARD_STDERR:
            sys.stderr = self.stream_to_method_converter(lambda m: self.queue_put(m))
            change_loggers_stream(self.original_stderr, sys.stderr)

    def restore_stdout_stderr(self):
        if self.FORWARD_STDOUT:
            sys.stdout = self.original_stdout
            change_loggers_stream(sys.stdout, self.original_stdout)

        if self.FORWARD_STDERR:
            sys.stderr = self.original_stderr
            change_loggers_stream(sys.stderr, self.original_stderr)


def change_loggers_stream(what, to):
    for logger_name in logging.Logger.manager.loggerDict:
        _logger = logging.getLogger(logger_name)
        for handler in _logger.handlers:
            if isinstance(handler, logging.StreamHandler) and handler.stream == what:
                handler.stream = to


class SyncAbstractWorker(AbstractWorker):
    def __init__(self, args: dict, queue_worker2server: AioQueue, queue_server2worker: AioQueue):
        super().__init__(args, queue_worker2server, queue_server2worker)
        self.stop_event = threading.Event()
        self.in_thread = None
        self.in_thread_callback = None

    def queue_put(self, data):
        self.queue_worker2server.put(data)
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # result = loop.run_until_complete(self.queue_worker2server.coro_put(data))
        # loop.close()
        # return result

    def queue_get(self):
        return self.queue_server2worker.get()
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # result = loop.run_until_complete(self.queue_server2worker.coro_get())
        # loop.close()
        # return result

    def on_in_thread(self, callback: Callable[[Any], Any]):
        self.in_thread_callback = callback
        if not self.in_thread:
            self.in_thread = threading.Thread(target=self._stdin_thread)
            self.in_thread.start()

    def _stdin_thread(self):
        while not self.stop_event.is_set():
            try:
                message = self.queue_server2worker.get(True, 0.2)
            except queue.Empty:
                continue
            if message:
                if self.in_thread_callback:
                    self.in_thread_callback(message)

    @classmethod
    def create(
            cls,
            args: dict,
            queue_worker2server: AioQueue,
            queue_server2worker: AioQueue,
            worker_key: str
    ):
        setproctitle.setproctitle(f"worker_{worker_key}")
        o = cls(args, queue_worker2server, queue_server2worker)
        result = 0
        o.replace_stdout_stderr()
        # noinspection PyBroadException
        try:
            o.run()
        except Exception:
            output = traceback.format_exc().split("\n")
            o.queue_put("\n".join(output[0:1] + output[2:]))
            result = 1
        o.stop(result)

    def stop(self, result: int):
        self.stop_event.set()
        if self.in_thread:
            self.in_thread.join()
        self.restore_stdout_stderr()
        self.queue_worker2server.put(WorkerResult(result))
        self.queue_worker2server.close()
        self.queue_server2worker.close()

    @abstractmethod
    def run(self):
        pass


class AsyncAbstractWorker(AbstractWorker):
    def __init__(self, args: dict, queue_worker2server: AioQueue, queue_server2worker: AioQueue):
        super().__init__(args, queue_worker2server, queue_server2worker)
        self.stream_to_method_converter = AsyncStreamToMethod

    async def queue_put(self, data):
        return await self.queue_worker2server.coro_put(data)

    async def queue_get(self):
        return await self.queue_server2worker.coro_get()

    @classmethod
    def create(
            cls,
            args: dict,
            queue_worker2server: AioQueue,
            queue_server2worker: AioQueue,
            worker_key: str
    ):
        setproctitle.setproctitle(f"worker_{worker_key}")
        o = cls(args, queue_worker2server, queue_server2worker)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(o.run_wrapper())
        loop.close()
        # asyncio.run(o.run_wrapper())

    async def run_wrapper(self):
        self.replace_stdout_stderr()
        result = 0
        # noinspection PyBroadException
        try:
            await self.run()
        except Exception:
            output = traceback.format_exc().split("\n")
            await self.queue_put("\n".join(output[0:1] + output[2:]))
            result = 1
        self.restore_stdout_stderr()
        await self.queue_worker2server.coro_put(WorkerResult(result))
        self.queue_worker2server.close()
        self.queue_server2worker.close()

        debug("Output in the end of run_wrapper()")
        remaining_tasks = asyncio.all_tasks()
        for task in remaining_tasks:
            debug(f"Unclosed task: {task}")

        debug(f"Active threads: {threading.enumerate()}")

    @abstractmethod
    async def run(self):
        pass


WorkerHandlerType = TypeVar('WorkerHandlerType', bound='WorkerHandler')


class WorkerHandler:
    def __init__(self, server: BaseServerType, worker_key: str, args: dict, worker_class=None):
        self.server = server
        self.worker_key = worker_key
        self.args = args
        self.queue_worker2server = AioQueue()
        self.queue_server2worker = AioQueue()
        self.worker_class = self.server.Worker if worker_class is None else worker_class
        self.process = AioProcess(
            target=self.worker_class.create, args=(
                args,
                self.queue_worker2server,
                self.queue_server2worker,
                worker_key
            )
        )
        self.readers = []

    def get_server(self) -> BaseServerType:
        return self.server

    def get_key(self):
        return self.worker_key

    def get_exit_code(self):
        if self.process.is_alive():
            return None
        return self.process.exitcode

    async def start(self):
        self.process.start()
        while self.process.is_alive():
            message = await self.queue_worker2server.coro_get()
            debug(f"WorkerHandler({self.worker_key}).received: {message}")

            readers = self.readers
            self.readers = []

            for reader in readers:
                await reader.put(message)

            if isinstance(message, WorkerResult):
                debug(f"WorkerResult: received {message}")
                self.queue_worker2server.close()
                self.queue_server2worker.close()
                break

        await self.process.coro_join()

        # Заглушка только для тестирования работы с AsyncAbstractWorker

        # try:
        #     # Ожидаем завершения процесса с тайм-аутом в 15 секунд
        #     await asyncio.wait_for(self.process.coro_join(), timeout=15.0)
        #     debug("Process completed within timeout.")
        # except asyncio.TimeoutError:
        #     # Тайм-аут, процесс не завершился в заданное время
        #     print("Timeout reached, terminating the process.")
        #     self.process.terminate()
        #     await self.process.coro_join()  # Дополнительно ожидаем завершения после terminate
        #     print("Process terminated.")
        #
        # print(f"Process alive?: {self.process.is_alive()}")

    async def read(self):
        reader = asyncio.Queue()
        self.readers.append(reader)
        return await reader.get()

    async def write(self, data):
        debug(f"WorkerHandler({self.worker_key}).write: {data}")
        await self.queue_server2worker.coro_put(data)

    async def on_exit(self, exit_code: int):
        readers = self.readers
        self.readers = []

        for reader in readers:
            await reader.put(WorkerResult(exit_code))

    def get_args(self) -> dict:
        return self.args


class BaseServer:
    class ClientHandler(AbstractClientHandler, ABC):
        pass

    class Worker(AsyncAbstractWorker, ABC):
        pass

    class WorkerHandler(WorkerHandler, ABC):
        pass

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.workers = {}

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )

        addr = server.sockets[0].getsockname()
        debug(f"started: {addr}")

        async with server:
            await server.serve_forever()

    async def handle_client(
            self,
            reader: StreamReader,
            writer: StreamWriter
    ):
        addr = writer.get_extra_info('peername')
        debug(f"Client connected {addr}")

        try:
            client = self.ClientHandler(reader, writer, self)
            await client.handle()
        except asyncio.CancelledError:
            debug(f"Cancelled connection with {addr}")
        except BaseException as e:
            output = traceback.format_exc().split("\n")
            error(f"Error with {addr}: {e}")
            error("\n".join(output[0:1] + output[2:]))
        finally:
            debug(f"Closed connection with {addr}")
            writer.close()
            try:
                await writer.wait_closed()
            except BrokenPipeError:
                pass
            except ConnectionResetError:
                pass

    async def start_process_manager(self):
        while True:
            keys = list(self.workers.keys())
            for worker_key in keys:
                worker = self.workers[worker_key]
                exit_code = worker.get_exit_code()
                if exit_code is not None:
                    debug(f"Process {worker_key} exited.")
                    self.workers.pop(worker_key)
                    await worker.on_exit(exit_code)
            await asyncio.sleep(1)

    async def run(self):
        await asyncio.gather(
            self.start_server(),
            self.start_process_manager()
        )

    def _create_worker(self, worker_key: str, args: dict, worker_class=None) -> WorkerHandlerType:
        if worker_key in self.workers:
            raise ValueError(f"Worker with name {worker_key} already exists")
        self.workers[worker_key] = self.WorkerHandler(self, worker_key, args, worker_class)
        return self.workers[worker_key]

    def create_worker(self, worker_key: str, args: dict, worker_class=None) -> WorkerHandlerType:
        worker = self._create_worker(worker_key, args, worker_class)
        asyncio.create_task(worker.start())
        return worker

    async def create_and_wait_worker(self, worker_key: str, args: dict, worker_class=None) -> WorkerHandlerType:
        worker = self._create_worker(worker_key, args, worker_class)
        await worker.start()
        return worker

    def get_worker(self, worker_key: str) -> WorkerHandlerType | None:
        if worker_key not in self.workers:
            return None
        return self.workers[worker_key]


class MicroserviceClientException(Exception):
    pass


class MicroserviceClient:
    def __init__(self, host: str, port: int = 5000):
        self.host = host
        self.port = port
        self.socket: Union[socket.socket, None] = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        self.socket.close()

    def send(self, msg: Any):
        serialized_msg = pickle.dumps(msg)

        # noinspection PyTypeChecker
        self.socket.sendall(struct.pack('>I', len(serialized_msg)))

        # noinspection PyTypeChecker
        self.socket.sendall(serialized_msg)

    def recv_all(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def receive(self):
        try:
            raw_msg_len = self.recv_all(4)
        except OSError:
            return None
        if not raw_msg_len:
            return None
        # noinspection PyTypeChecker
        raw_msg_len = struct.unpack('>I', raw_msg_len)[0]
        try:
            # noinspection PyTypeChecker
            return pickle.loads(self.recv_all(raw_msg_len))
        except OSError:
            return None
