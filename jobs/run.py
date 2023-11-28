import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description='Run a job.')
    parser.add_argument('job', help='Name of the job to run',
                        choices=["mongoinit.py", "postgresinit.py"])

    args = parser.parse_args()

    exit_code = subprocess.run(['python', args.job]).returncode
    exit(exit_code)


if __name__ == '__main__':
    main()
