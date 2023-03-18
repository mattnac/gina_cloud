import click, zipfile
from colorlog import ColoredFormatter
import logging
from os import listdir
from os.path import isfile, join
import tail
from xml.etree import ElementTree
from pygina import Trigger, TriggerList
import inflection


def merge(xml_list):
    xml_data = None
    for xml_string in xml_list:
        data = ElementTree.fromstring(xml_string)
        if xml_data is None:
            xml_data = data
        else:
            xml_data.extend(data)
    if xml_data is not None:
        return xml_data.findall(".//Trigger")


def configure_logging(verbose):
    log_level = 50 - ((1 + verbose) * 10)
    logging.root.setLevel(log_level)
    log_format = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
    formatter = ColoredFormatter(log_format)

    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)

    logging.root.setLevel(log_level)
    logging.root.addHandler(stream)


@click.group()
@click.option("--triggers-dir", "-T", help="Directory with gina triggers",
              type=click.Path(dir_okay=True, file_okay=False, resolve_path=True), default="triggers", show_default=True)
@click.option('--log-file', '-L', default="/home/fishdaemon/EQLite/Logs/eqlog_Karolus_P1999Green.txt", help="Log file",
              required=True,
              show_default=True, type=click.Path(dir_okay=False, file_okay=True, resolve_path=True))
@click.option("--verbose", "-v", count=True, default=(logging.WARNING / 20),
              help="controls log level")
@click.pass_context
def cli(ctx, triggers_dir, log_file, verbose):
    configure_logging(verbose)
    ctx.ensure_object(dict)

    load_triggers(triggers_dir)
    ctx.obj["log_file"] = log_file


def load_triggers(dir):

    files = get_file_list(dir)
    xml_data = list()
    for f in files:
        with zipfile.ZipFile(f, 'r') as zip_ref:
            with zip_ref.open('ShareData.xml') as xml_file:
                xml_data.append(xml_file.read())
    TriggerList.append(Trigger(
        name="Zone Timer",
        trigger_text="(You have slain (?<mob>.*)!)|((?<mob>.*) has been slain by .*!)",
        timer_type="Timer",
        timer_name="${mob}",
        timer_duration=640,
        category="timers",
        restart_based_on_timer_name=False

    ))
    for trigger in merge(xml_data):
        args = dict()
        for node in trigger.findall("./"):
            args[inflection.underscore(node.tag)] = node.text
        TriggerList.append(Trigger(**args))



def get_file_list(dir):
    return [
        "{}/{}".format(dir, f) for f in listdir(dir) if isfile(join(dir, f))
    ]


@cli.command("start")
@click.pass_context
def start(ctx):
    t = tail.Tail(ctx.obj["log_file"])
    t.register_callback(check_pattern)
    t.follow(s=0.1)


def check_pattern(line):
    #click.echo(line, nl=False)
    for t in TriggerList:

        if t.match(line):
            click.echo("MATCH {}".format(t.name))


if __name__ == '__main__':
    cli()
