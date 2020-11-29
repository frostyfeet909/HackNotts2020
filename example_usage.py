import tell_me_done
from time import sleep


def do_something(some_setting):
    # Some task that takes a long time
    print("Started!")
    print("Running with: %i" % some_setting)
    sleep(some_setting)
    print("Done!")


def main():
    some_setting = 5
    notifier = tell_me_done.Notifier()

    # Do it forever :O
    while some_setting != "3":
        do_something(int(some_setting))

        notifier.notify(done=True)

        some_input = tell_me_done.get_vars()
        while some_input is None:
            some_input = tell_me_done.get_vars()
            sleep(2)
        some_setting = some_input

    notifier.shutdown()
    print("Example finished!")


if __name__ == "__main__":
    main()
