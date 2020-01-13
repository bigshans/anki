# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Tools for extending Anki.

A hook takes a function that does not return a value.

A filter takes a function that returns its first argument, optionally
modifying it.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List

import decorator

from anki.cards import Card

# New hook/filter handling
##############################################################################
# The code in this section is automatically generated - any edits you make
# will be lost. To add new hooks, see ../tools/genhooks.py
#
# To use an existing hook such as leech_hook, you would call the following
# in your code:
#
# from anki import hooks
# hooks.leech_hook.append(myfunc)
#
# @@AUTOGEN@@

leech_hook: List[Callable[[Card], None]] = []
mod_schema_filter: List[Callable[[bool], bool]] = []
odue_invalid_hook: List[Callable[[], None]] = []


def run_leech_hook(card: Card) -> None:
    for hook in leech_hook:
        try:
            hook(card)
        except:
            # if the hook fails, remove it
            leech_hook.remove(hook)
            raise
    # legacy support
    runHook("leech", card)


def run_mod_schema_filter(proceed: bool) -> bool:
    for filter in mod_schema_filter:
        try:
            proceed = filter(proceed)
        except:
            # if the hook fails, remove it
            mod_schema_filter.remove(filter)
            raise
    return proceed


def run_odue_invalid_hook() -> None:
    for hook in odue_invalid_hook:
        try:
            hook()
        except:
            # if the hook fails, remove it
            odue_invalid_hook.remove(hook)
            raise


# @@AUTOGEN@@

# Legacy hook handling
##############################################################################

_hooks: Dict[str, List[Callable[..., Any]]] = {}


def runHook(hook: str, *args) -> None:
    "Run all functions on hook."
    hookFuncs = _hooks.get(hook, None)
    if hookFuncs:
        for func in hookFuncs:
            try:
                func(*args)
            except:
                hookFuncs.remove(func)
                raise


def runFilter(hook: str, arg: Any, *args) -> Any:
    hookFuncs = _hooks.get(hook, None)
    if hookFuncs:
        for func in hookFuncs:
            try:
                arg = func(arg, *args)
            except:
                hookFuncs.remove(func)
                raise
    return arg


def addHook(hook: str, func: Callable) -> None:
    "Add a function to hook. Ignore if already on hook."
    if not _hooks.get(hook, None):
        _hooks[hook] = []
    if func not in _hooks[hook]:
        _hooks[hook].append(func)


def remHook(hook, func) -> None:
    "Remove a function if is on hook."
    hook = _hooks.get(hook, [])
    if func in hook:
        hook.remove(func)


# Monkey patching
##############################################################################
# Please only use this for prototyping or for when hooks are not practical,
# as add-ons that use monkey patching are more likely to break when Anki is
# updated.
#
# If you call wrap() with pos='around', the original function will not be called
# automatically but can be called with _old().
def wrap(old, new, pos="after") -> Callable:
    "Override an existing function."

    def repl(*args, **kwargs):
        if pos == "after":
            old(*args, **kwargs)
            return new(*args, **kwargs)
        elif pos == "before":
            new(*args, **kwargs)
            return old(*args, **kwargs)
        else:
            return new(_old=old, *args, **kwargs)

    def decorator_wrapper(f, *args, **kwargs):
        return repl(*args, **kwargs)

    return decorator.decorator(decorator_wrapper)(old)
