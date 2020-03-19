import tqdm
import sys

def count_lines(infile):
    if isinstance(infile, str):
      with open(infile) as f:
        return count_lines(f)
    n = 0
    prev = None
    while True:
      try:
        for line in infile:
          n += 1
          prev = line
          #print(n)
        break
      except UnicodeDecodeError:
        if verbose:
          sys.stderr.write('Error on line %d after %s\n' % (n+1, repr(prev)))
        if not ignore_errors:
          raise
    return n

def for_each_line(infile, total=None, verbose=True, ignore_errors=True, message=None):
    if isinstance(infile, str):
      with open(infile) as f:
        for i, line in for_each_line(f, total=total, verbose=verbose, ignore_errors=ignore_errors, message=message):
          yield i, line
    #import pdb; pdb.set_trace()
    n = count_lines(infile) if total is None else total
    #import pdb; pdb.set_trace()
    if message:
      print('%s %d lines...' % (message, n))
    i = 0
    if isinstance(infile, list):
      for line in tqdm.tqdm(infile, total=n) if verbose else infile:
        yield i, line
        i += 1
    else:
      while True:
        try:
          n -= i
          for line in tqdm.tqdm(infile, total=n) if verbose else infile:
            yield i, line
            i += 1
          break
        except UnicodeDecodeError:
          pass

def ensure_open(filename, *args, **kws):
  while True:
    try:
      return open(filename, *args, **kws)
    except Exception as exc:
      if not isinstance(exc, FileNotFoundError):
        import traceback
        traceback.print_exc()
      sys.stderr.write('Failed to open file: %s. Trying again in 1.0 seconds...\n' % filename)
      time.sleep(1.0)

import numpy as np
import io

def tokens_to_buffer(chunks, stride):
  assert stride in [2, 4]
  tokens = np.array(chunks, dtype=np.uint16 if stride == 2 else np.int32)
  out = io.BytesIO()
  tokens.tofile(out)
  return out.getvalue()

def tokens_from_buffer(data, stride):
  assert stride in [2, 4]
  return np.frombuffer(data, dtype=np.uint16 if stride == 2 else np.int32)

def tokens_to_file(out, chunks, stride):
  assert stride in [2, 4]
  tokens = np.array(chunks, dtype=np.uint16 if stride == 2 else np.int32)
  tokens.tofile(out)

def tokens_from_file(f, stride):
  assert stride in [2, 4]
  return np.fromfile(f, dtype=np.uint16 if stride == 2 else np.int32)
