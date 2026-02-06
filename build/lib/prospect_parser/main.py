from prospect_parser.ProspectParser import ProspectParser
import sys

def main() -> None:
    parser = ProspectParser(sys.argv[1]) if len(sys.argv) > 1 else ProspectParser()
    parser.run()


if __name__ == '__main__':
    main()