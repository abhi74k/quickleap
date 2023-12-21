import pygetwindow as gw


def get_all_open_windows_title():
    # Get a list of all open windows
    windows = gw.getAllTitles()
    return windows


def get_all_windows():
    windows = gw.getAllWindows()
    return windows


def filter_windows(filter_fn):
    windows = get_all_windows()

    ret = []
    for window in windows:
        if filter_fn(window.title):
            ret.append((window.title, window))

    return ret


def switch_to_window(title):
    try:
        windows = gw.getAllWindows()
        # Find the window with the specified title
        window = gw.getWindowsWithTitle(title)[0]  # This will get the first window that matches the title
        if window is not None:
            # If the window is found, activate it
            window.activate()
            return True
        else:
            print(f"No window with title '{title}' found.")
            return False
    except IndexError:
        # No window with that title was found
        print(f"No window with title '{title}' found.")
        return False


if __name__ == '__main__':
    # Example usage: switch to a window with 'Notepad' in the title
    switch_to_window('Outline for 224W Medium')
