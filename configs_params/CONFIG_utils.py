# STEPS
def steps(start, end, interval):
  """ 
    Similar to range() but supports decimal number
    end is not included in the returned list
  """

  s = []
  val = start

  while val < end:
    s.append(val)
    val += interval

  return s