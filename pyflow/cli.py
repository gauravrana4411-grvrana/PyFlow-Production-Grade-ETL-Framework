import argparse


parser = argparse.ArgumentParser(
    description="PyFlow ETL Framework"
)

parser.add_argument(
    '--config',
    required=True
)

parser.add_argument(
    '--mode',
    default='full'
)

args = parser.parse_args()

print(args)