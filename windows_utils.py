import pygetwindow as gw
import fuzzystringmatch as fsm


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


def get_window_candidate_list_with_fuzzy_regex(query_string):
    try:
        windows = get_all_windows()
        window_titles = [window.title for window in windows]
        matched_window_titles = fsm.fuzzy_regex_match_string_list(query_string, window_titles)
        return matched_window_titles
    except Exception:
        print(f"Something went wrong....")
        return []


def get_window_candidate_list_with_fuzzy_approx_match(query_string):
    try:
        windows = get_all_windows()
        window_titles = [window.title for window in windows]
        matched_window_titles = fsm.fuzzy_approx_match_string_list(query_string, window_titles)
        return matched_window_titles
    except Exception:
        return []


if __name__ == '__main__':
    # Switch to window based the window title
    # switch_to_window('Outline for 224W Medium')

    # c224w wouldn't work.
    ret = get_window_candidate_list_with_fuzzy_regex("cs224w")
    print(f"Candidate list with fuzzy regex: \n{ret}")

    # c224w would work since we use approximate string matching
    ret = get_window_candidate_list_with_fuzzy_approx_match("c224w")
    print(f"Candidate list with approximate fuzzy matching : \n {ret}")
