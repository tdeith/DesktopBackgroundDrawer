'''
Created on Apr 13, 2014

@author: Taylor
'''
import unittest
import ColourBucket

midR = 4
midG = 4
midB = 4

R1 = 0.5
G1 = 0.5
B1 = 0.5

R2 = 6.5
G2 = 6.5
B2 = 6.5

R3 = 3
G3 = 3
B3 = 3

x = 1
y = 1

size = 3
limit = 1

class Test(unittest.TestCase):
    
    print "Testing colour buckets..."
    
    def testBucketCreation(self):
        bucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        self.assertEqual(bucket.Population, 0)
        self.assertEqual(len(bucket.Children), 0)
        self.assertIsNone(bucket._indexedChildren[0])
        
    def testBucketAdding(self):
        ParentBucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        ColourBucket.AddColour(ParentBucket, (R1, G1, B1, x, y, 0))
        bucket = ParentBucket
        for i in xrange(size-limit):                                # @UnusedVariable
            self.assertEqual(bucket.Population, 1)
            self.assertIs(bucket._indexedChildren[0], bucket.Children[0])
            self.assertEqual(bucket.Size-1, bucket.Children[0].Size)
            bucket = bucket.Children[0]
            self.assertIsInstance(bucket, ColourBucket.ColourBucket)
        self.assertEqual(bucket.Children[0], [R1, G1, B1, x, y, 0])
        self.assertEqual(bucket.Population, 1)
        
        ColourBucket.AddColour(ParentBucket, (R2, G2, B2, x, y, 0))
        bucket = ParentBucket
                
        self.assertEqual(ParentBucket.Population, 2)
        for i in xrange(size-limit):                                # @UnusedVariable
            self.assertIs(bucket._indexedChildren[7], bucket.Children[-1])
            self.assertEqual(bucket.Size-1, bucket.Children[-1].Size)
            bucket = bucket.Children[-1]
            self.assertIsInstance(bucket, ColourBucket.ColourBucket)
        self.assertEqual(bucket.Children[0], [R2, G2, B2, x, y, 0])
        self.assertEqual(bucket.Population, 1)
        
        ColourBucket.AddColour(ParentBucket, (R1, G1, B1, x, y, 0))
        self.assertEqual(ParentBucket.Population, 3)
        
        bucket = ParentBucket.Children[0].Children[0]
        self.assertEqual(len(bucket.Children), 2)
        self.assertEqual(bucket.Population, 2)

    def testBucketRemoval(self):
        parentBucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        ColourBucket.AddColour(parentBucket, (R1, G1, B1, x, y, 0))
        ColourBucket.AddColour(parentBucket, (R1, G1, B1, x, y, 0))
        ColourBucket.AddColour(parentBucket, (R2, G2, B2, x, y, 0))
        self.assertEqual(parentBucket.Population, 3)

        ColourBucket.RemoveColour(parentBucket, (R1, G1, B1, x, y, 0))
        bucket = parentBucket.Children[0].Children[0]
        self.assertEqual(bucket.Population, 1)
        self.assertEqual(len(bucket.Children), 1)
        
        ColourBucket.RemoveColour(parentBucket, (R1, G1, B1, x, y, 0))
        self.assertIs(parentBucket._indexedChildren[0], None)
        self.assertEqual(parentBucket.Population, 1)
        bucket = parentBucket.Children[0].Children[0]
        self.assertEqual(bucket.Children[0], [R2, G2, B2, x, y, 0])
        
    def testBucketUpdate(self):
        parentBucket = ColourBucket.ColourBucket(midR, midG, midB, size, limit)
        ColourBucket.AddColour(parentBucket, (R1, G1, B1, x, y, 0))
        ColourBucket.AddColour(parentBucket, (R1, G1, B1, x, y, 0))
        ColourBucket.AddColour(parentBucket, (R2, G2, B2, x, y, 0))
        self.assertEqual(parentBucket.Population, 3)
        
        ColourBucket.UpdateColour(parentBucket, (R1, G1, G1), (R2, G2, B2), (x, y), 0)
        oldBucket = parentBucket.Children[0].Children[0]
        updatedBucket = parentBucket.Children[-1].Children[-1]
        self.assertEqual(parentBucket.Population, 3)
        self.assertEqual(updatedBucket.Population, 2)
        self.assertEqual(len(updatedBucket.Children), 2)
        self.assertEqual(oldBucket.Population, 1)
        self.assertEqual(len(oldBucket.Children), 1)
        
        ColourBucket.UpdateColour(parentBucket, (R1, G1, B1), (R3, G3, B3), (x, y), 0)
        updatedBucket = parentBucket.Children[0].Children[-1]
        self.assertIs(parentBucket._indexedChildren[0]._indexedChildren[0], None)
        self.assertEqual(parentBucket._indexedChildren[0]._indexedChildren[7], updatedBucket)
        self.assertEqual(updatedBucket.Children[0], [R3, G3, B3, x, y, 0])
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testBucketCreation']
    unittest.main()