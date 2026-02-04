from prospect_parser.parser import ProspectParser
import sys

def main():
    parser = ProspectParser()
    if len(sys.argv) > 1:
        parser.category = sys.argv[1]
    parser.fill_storage()
    parser.create_json()


if __name__ == '__main__':
    main()