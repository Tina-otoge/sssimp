import importlib
import logging
from pathlib import Path
import shutil

import sssimp
from sssimp import config
from sssimp.utils import mkdir, path_strip


logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)


def run_generators():
    modules = set()
    for file in (sssimp.APP_DIR / 'generators').glob('**/*.py'):
        module_str = path_strip(file).replace('/', '.')[:-len('.py')]
        module = importlib.import_module(f'.{module_str}', package='sssimp')
        if hasattr(module, 'main'):
            modules.add(module)
        if hasattr(module, 'prepare'):
            logging.info(f'Preparing {module.__name__}')
            module.prepare()
    for module in modules:
        logging.info(f'Running {module.__name__}')
        module.main()


def is_ignored(path: Path):
    for ignore_path in sssimp.IGNORE_ASSETS:
        if ignore_path == str(path):
            return ignore_path
        if Path(ignore_path).is_dir() and ignore_path in {str(x) for x in path.parents}:
            return ignore_path


def copy_assets():
    logging.debug(f'Ignore list: {sssimp.IGNORE_ASSETS}')
    for file in sssimp.CONTENT_DIR.glob('**/*'):
        if not file.is_file():
            continue
        relative_path = path_strip(file, sssimp.CONTENT_DIR)
        if (match := is_ignored(file)):
            logging.info(
                f'Ignoring asset {relative_path} because it matches'
                f' "{match}" from ignore list'
            )
            continue
        out_file = sssimp.OUTPUT_DIR / relative_path
        mkdir(out_file)
        logging.info(f'Copying raw asset {file} -> {out_file}')
        shutil.copyfile(file, out_file)


if __name__ == '__main__':
    if config.CLEAN_OUTPUT and sssimp.OUTPUT_DIR.exists():
        try:
            shutil.rmtree(sssimp.OUTPUT_DIR)
        except Exception:
            for f in sssimp.OUTPUT_DIR.glob('*'):
                shutil.rmtree(f)
        logging.info(f'Deleted {sssimp.OUTPUT_DIR}')
    logging.info('Running generators')
    run_generators()
    logging.info('Copying raw assets')
    copy_assets()
    print()
    print(f'Generation finished, open {sssimp.OUTPUT_DIR.resolve().as_uri()} in browser')
