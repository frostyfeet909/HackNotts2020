import tell_me_done
from time import sleep


def do_something(some_setting):
    # Some task that takes a long time
    print("Started!")
    sleep(some_setting)
    print("Done!")


def main():
    some_setting = 10
    notifier = tell_me_done.Notifier()
    condition = "boop"

    # Do it forever :O
    while condition != "":
        do_something(some_setting)
        notifier.notify(done=True)
        condition = input(">> ")

    notifier.shutdown()
    print("Example finished!")


if __name__ == "__main__":
    main()
