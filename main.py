import argparse
from sum import sum
from sub import sub




if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--X", type=int, required=True)
    parser.add_argument("--Y", type=int, required=True)
    parser.add_argument("--opr", type=str, default="sum", help="math ops: sum | sub")


    args = parser.parse_args()

    match args.opr:
        case "sum":
            print(sum(args.X, args.Y))

        case "sub":
            print(sub(args.X, args.Y))
        case _:
            print(f"Invalid operation {args.opr}")
