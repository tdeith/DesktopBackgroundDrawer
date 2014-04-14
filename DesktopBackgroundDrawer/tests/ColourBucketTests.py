'''
Created on Apr 13, 2014

@author: Taylor
'''
import unittest
import ColourBucket

midR = 4
midG = 4
midB = 4

newR = 0.5
newG = 0.5
newB = 0.5

x = 0
y = 0

size = 3
limit = 1

class Test(unittest.TestCase):


    def testBucketCreation(self):
        bucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        self.assertEqual(bucket.Population, 0)
        self.assertEqual(len(bucket.Children), 0)
        self.assertIsNone(bucket._indexedChildren[0])
        
    def testBucketAdding(self):
        bucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        ColourBucket.AddColour(bucket, (newR, newG, newB, x, y, 0))
        self.assertIsInstance(bucket._indexedChildren[0], ColourBucket.ColourBucket)
        self.assertIsInstance(bucket.Children[0], ColourBucket.ColourBucket)
        self.assertIsInstance(bucket.Children[0].Children[0], ColourBucket.ColourBucket)
        self.assertIsInstance(bucket.Children[0].Children[0].Children[0], ColourBucket.ColourBucket)
        self.assertEqual(bucket.Children[0].Children[0].Children[0].Children[0], [newR, newG, newB, x,y,0])
        self.assertEqual(bucket.Population, 1)
        self.assertEqual(bucket.Size-1, bucket._indexedChildren[0].Size)
        ColourBucket.AddColour(bucket, (newR, newG, newB, x, y, 0))
        self.assertEqual(bucket.Population, 2)
        ColourBucket.AddColour(bucket, (4, 4, 4, x, y, 0))

    def testBucketRemoval(self):
        bucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        ColourBucket.AddColour(bucket, (newR, newG, newB, x, y, 0))
        ColourBucket.AddColour(bucket, (newR, newG, newB, x, y, 0))
        ColourBucket.AddColour(bucket, (newR, newG, newB, x, y, 0))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBucketCreation']
    unittest.main()