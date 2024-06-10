import uvicorn
import argparse

def dev():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)


def start():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the backend")
    parser.add_argument("mode", type=str, help="start mode")
    args = parser.parse_args()
    if args.mode == 'dev':
        dev()
    elif args.mode == 'start':
        start()
