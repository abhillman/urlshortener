# vim: set encoding=utf-8 shiftwidth=2 tabstop=2 expandtab:

import os
import logging
import sys
from optparse import OptionParser

LOG_FILE = '/var/log/taskrunner.log'


def main():
  logging.basicConfig(filename = LOG_FILE, level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
  run_task()


def run_task():
  usage = '%prog -c <command> -l <lockfile> [-t <threshold> -f <file>]'
  
  parser = OptionParser(usage = usage)
  parser.add_option('-c', '--command', help = 'command to run', metavar = 'COMMAND', dest = 'command')
  parser.add_option('-l', '--lockfile', help = 'path to lock file', metavar = 'FILE', dest = 'lockfile')
  parser.add_option('-t', '--threshold', help = 'failure threshold', metavar = 'NUMBER', dest = 'threshold')
  parser.add_option('-f', '--counter-file', help = 'counter filer to keep track of failed attempts', metavar = 'FILE', dest = 'counter_file')
  (options, args) = parser.parse_args()
  
  if (not options.command) or (not options.lockfile) or (options.threshold and not options.counter_file):
    parser.print_usage()
    logging.error('Got no or invalid arguments, exiting.')
    sys.exit(1)

  if create_lockfile(options.lockfile):
    # Remove failure counter
    if options.threshold and options.counter_file\
    and os.path.exists(options.counter_file):
      os.remove(options.counter_file)

    # Run the command
    os.system(options.command)
    logging.info('Successfully ran: ' + options.command)

    # Remove lock
    try:
      remove_lockfile(options.lockfile)
    except BaseException as e:
      logging.error('Could not delete lockfile ' + repr(options.lockfile) + ' ' + e)
      sys.exit(1) 
    sys.exit(0)
  else:
    # A lockfile exists
    if options.threshold and options.counter_file:
      if check_threshold(options.counter_file, options.threshold):
        logging.error('Hit failure threshold. See next error for details. Command = ' + repr(options.command))
      else:
        return

    logging.error('Tried to run command, but lockfile exists. Command = ' + repr(options.command))

def check_threshold(counter_file, threshold):
  '''
  Checks if the number in a counter file is bigger than a threshold

  Returns False if the number is smaller, True if its greater or equal. When true
  is returned, the value in the counter file will be reset to zero. 
  The counter file will be created if it does'nt exist.
  '''
 
  threshold = int(threshold)
  attempts = 0

  # Try to read the attempts file
  try:
    f = open(counter_file, 'r+b')
    attempts = int(f.read())
  except IOError as e:
    if e.errno == 2:
      # Create the file if it doesn't exist, and write attempts
      f = open(counter_file, 'w+b')
      f.write(str(attempts))
    else:
      raise e

  # Increment attempts
  attempts += 1

  f = open(counter_file, 'w+b')

  if attempts >= threshold:
    # Reset counter
    f.write('0')
    return True
  else:
    # Write attempts
    f.write(str(attempts))
    return False

def create_lockfile(path):
  '''
  Create a safe lockfile

  This function creates safe lockfiles by using link, which is atomic.
  '''
  temp_node = path + '.tmp'

  def false_on_existing_file(e):
    if e.errno == 17:
      return False
    else:
      raise

  try:
    os.mknod(temp_node)
  except OSError as e:
    return false_on_existing_file(e)

  try:
    os.link(temp_node, path)
    ret = True
  except OSError as e:
    ret = false_on_existing_file(e)
  finally:
    os.remove(temp_node)

  return ret

def remove_lockfile(path):
  '''
  Remove a lockfile
  '''
  os.remove(path)

if __name__ == '__main__':
  main()

