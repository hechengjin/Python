import unittest

def class_001():
   print(f'class 001')  # Press Ctrl+F8 to toggle the breakpoint.


def funAddOne(x):
   return x + 1


class Class001Test(unittest.TestCase):
   def testAddOne(self):
      self.assertEqual(funAddOne(3), 4)