from flask_script import Manager
from whiskyton.models import Whisky
from whiskyton.helpers.charts import Chart

ChartsCommand = Manager(usage='Manage chart cache')


@ChartsCommand.command
def delete():
    """Delete all cached charts"""
    folder_path = (Chart()).cache_path()
    if not folder_path.exists():
        folder_path.mkdir()
    folder = folder_path.listdir()
    count = 0
    size = 0
    total = float(len(folder))
    for f in folder:
        print('%s Deleting %s (%s)' % (percent((count / total)),
                                       f.absolute(),
                                       file_size(f.size())))
        if f.isfile():
            count += 1
            size += f.size()
            f.remove()
    print('%s cached charts deleted (%s)' % (count, file_size(size)))


@ChartsCommand.command
def create():
    """Create all charts as cache"""

    # support vars
    different_tastes = list()
    count = 0
    size = 0

    # get whiskies
    whiskies = Whisky.query.all()
    for whisky in whiskies:
        tastes = whisky.get_tastes()
        if tastes not in different_tastes:
            different_tastes.append(tastes)
    total = len(different_tastes) * (len(different_tastes) - 1.0)

    # combination
    for reference in different_tastes:
        for whisky in different_tastes:
            if whisky != reference:
                chart = Chart(reference=reference, comparison=whisky)
                file_name = chart.cache_name(True)
                if file_name.exists():
                    file_name.remove()
                chart.cache()
                size += file_name.size()
                count += 1
                print('%s Created %s (%s)' % (percent(count / total),
                                              file_name.absolute(),
                                              file_size(file_name.size())))
    print('%s charts created (%s)' % (count, file_size(size)))


@ChartsCommand.command
def cache():
    """List cached charts"""
    folder_path = (Chart()).cache_path()
    if not folder_path.exists():
        folder_path.mkdir()
    folder = folder_path.listdir()
    count = 0
    size = 0
    for f in folder:
        if f.isfile():
            print('%s (%s)' % (f.absolute(), file_size(f.size())))
            count += 1
            size += f.size()
    print('%s cached files (%s)' % (count, file_size(size)))


def file_size(size):
    sizes = {
        9: 'Gb',
        6: 'Mb',
        3: 'Kb',
        0: 'bytes'
    }
    for i in [9, 6, 3, 0]:
        if size >= 10 ** i:
            return '{:.1f}'.format(size / (10.0 ** i)) + sizes[i]
    return '0 %s' % sizes[0]


def percent(number):
    return '{:.1f}%'.format(number * 100)
