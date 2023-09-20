#Copyright 2023 izharus
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

from log_wizard.logger_manager import DefaultConfig
from log_wizard.logger_manager import log
log = log()

def main():
    """
    Example usage:
    """
    DefaultConfig(log_dir = 'data/log')
    proc_id = "12345"
    log.info("some info")
    log.error("some error")
    log.debug("some debug")
    log.critical("some critical")
    with log.insert_proc_id(proc_id):
        log.info("here should be proc id")
        with log.insert_func_name():
            log.info("here also should be proc id and a func name")
            with log.insert_func_name():
                log.info("here also should be proc id and a func name")
    with log.insert_func_name():
        log.info("here should be only a func name")
        with log.insert_proc_id(proc_id):
            log.info("here also should be proc id and a func name")
    log.info("some info")
if __name__ == '__main__':
    main()


