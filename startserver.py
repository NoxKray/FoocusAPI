from fooocusapi.base_args import add_base_args

    parser = argparse.ArgumentParser()
    add_base_args(parser, True)

    args, _ = parser.parse_known_args()
    install_dependents(skip=args.skip_pip)

    from fooocusapi.args import args

    if prepare_environments(args):
        sys.argv = [sys.argv[0]]

        # Load pipeline in new thread
        preload_pipeline_thread = Thread(target=preload_pipeline, daemon=True)
        preload_pipeline_thread.start()

        # Start task schedule thread
        from fooocusapi.worker import task_schedule_loop

        task_schedule_thread = Thread(target=task_schedule_loop, daemon=True)
        task_schedule_thread.start()

        # Start api server
        from fooocusapi.api import start_app

        start_app(args)
