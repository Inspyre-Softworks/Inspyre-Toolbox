from .arguments import Arguments

PARSED_ARGS = Arguments().parsed


def main():
    return getattr(PARSED_ARGS, 'NEW PATH')

    # add_to_path(PARSED_ARGS.new_path, do_not_notify=PARSED_ARGS.do_not_notify, profile_file=PARSED_ARGS.file)
