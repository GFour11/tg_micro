import asyncio
import argparse

from importlib import import_module


def main():
    parser = argparse.ArgumentParser(description='Run microservice')

    parser.add_argument('--name', type=str, help='Microservice name', required=True)
    parser.add_argument('--host', type=str, help='Microservice host', required=False, default="0.0.0.0")
    parser.add_argument('--port', type=int, help='Microservice port', required=False, default=5000)

    args = parser.parse_args()

    ms_name = args.name

    try:
        module = import_module(ms_name)
    except ModuleNotFoundError:
        raise ValueError('Invalid microservice name')

    if not hasattr(module, 'Server'):
        raise ValueError(f"Invalid microservice {ms_name}: Server class not found")

    microservice = module.Server(
        host=args.host,
        port=args.port,
    )
    asyncio.run(microservice.run())


if __name__ == '__main__':
    main()
