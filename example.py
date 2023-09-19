from src.logger_manager import log, DefaultConfig


def main():
    """
    Example usage:
    """
    DefaultConfig(log_dir = 'data/log')
    proc_id = "12345"
    log().info("some info")
    log().error("some error")
    log().debug("some debug")
    log().critical("some critical")
    with log().insert_proc_id(proc_id):
        log().info("here should be proc id")
        with log().insert_func_name():
            log().info("here also should be proc id and a func name")
            with log().insert_func_name():
                log().info("here also should be proc id and a func name")
    with log().insert_func_name():
        log().info("here should be only a func name")
        with log().insert_proc_id(proc_id):
            log().info("here also should be proc id and a func name")
    log().info("some info")
if __name__ == '__main__':
    main()


