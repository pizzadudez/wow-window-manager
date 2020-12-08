from mouse import _listener, ButtonEvent, LEFT, RIGHT, MIDDLE, X, X2, UP, DOWN, DOUBLE

# def on_button(
#     callback, args=(), buttons=(LEFT, MIDDLE, RIGHT, X, X2), types=(UP, DOWN, DOUBLE)
# ):
#     """ Invokes `callback` with `args` when the specified event happens. """
#     if not isinstance(buttons, (tuple, list)):
#         buttons = (buttons,)
#     if not isinstance(types, (tuple, list)):
#         types = (types,)

#     def handler(event):
#         if isinstance(event, ButtonEvent):
#             if event.event_type in types and event.button in buttons:
#                 # callback(*args)
#                 # vlad
#                 callback(event, *args)
#                 # /vlad

#     _listener.add_handler(handler)
#     return handler


def on_button_modified(
    callback, args=(), buttons=(LEFT, MIDDLE, RIGHT, X, X2), types=(UP, DOWN, DOUBLE)
):
    """ Invokes `callback` with `args` when the specified event happens. """
    if not isinstance(buttons, (tuple, list)):
        buttons = (buttons,)
    if not isinstance(types, (tuple, list)):
        types = (types,)

    def handler(event):
        if isinstance(event, ButtonEvent):
            if event.event_type in types and event.button in buttons:
                callback(event, *args)

    _listener.add_handler(handler)
    return handler


def on_click_modified(callback, args=()):
    """ Invokes `callback` with `args` when the left button is clicked. """
    return on_button_modified(callback, args, [LEFT], [UP])


if __name__ == "__main__":
    print(_listener)
