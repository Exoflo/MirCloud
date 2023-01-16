from django.db import models
import json
import numpy as np
import math
import operator
import cv2

# Create your models here.


class User(models.Model):
    isLogged = models.BooleanField(default=False)
    identifiant_secret = models.CharField(max_length=16, default='')
        
    
    def setAttributes(self, isLogged, identifiant_secret):
        self.isLogged = isLogged
        self.identifiant_secret = identifiant_secret

    def __str__(self):
        return "Instance of <User>"

class InputImage(models.Model):

    name = models.CharField(max_length=256)
    path = models.CharField(max_length=256, unique = True)
    family = models.CharField(max_length = 256, unique = True)
    
    def __str__(self):
        return f' name: {self.name}, family : {self.family}'

class Descripteur(models.Model):
    name = models.CharField(max_length=2500)
    tempsIndexation = models.FloatField(default=0)
    taille = models.FloatField(default=0)
    tempsRecherche = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Requete(models.Model):
    imageName = models.CharField(max_length=250)
    imageFamily = models.CharField(max_length = 250)
    results = models.JSONField
    r20 = models.FloatField(default = 0)
    r50 = models.FloatField(default = 0)
    r100 = models.FloatField(default = 0)
    rmax = models.FloatField(default = 0)
    p20 = models.FloatField(default = 0)
    p50 = models.FloatField(default = 0)
    p100 = models.FloatField(default = 0)
    pmax = models.FloatField(default = 0)
    ap20 = models.FloatField(default = 0)
    ap50 = models.FloatField(default = 0)
    ap100 = models.FloatField(default = 0)
    apmax = models.FloatField(default = 0)
    map20 = models.FloatField(default = 0)
    map50 = models.FloatField(default = 0)
    map100 = models.FloatField(default = 0)
    mapmax = models.FloatField(default = 0)

    def __str__(self):
        tmp = json.load(self.results)
        return f"This search has returned {len(tmp)} results"


class Top(models.Model):
    value = models.IntegerField(default=0)
    string = models.CharField(max_length=100)

    def __str__(self):
        return self.string

class Norme(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


    def l1Distance(l1,l2): 
        length = min(len(l1),len(l2)) 
        return sum([abs(a-b) for a,b in zip(l1[:length],l2[:length])])

    def euclidianDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        return (sum([(a-b)**2 for a,b in zip(l1[:length],l2[:length])]))**0.5

    def correlationDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        l1mean = sum(l1[:length])/length
        l2mean = sum(l2[:length])/length

        L1 = [x-l1mean for x in l1[:length]]
        L2 = [x-l2mean for x in l2[:length]]
        return 1 - sum([a*b for a,b in zip(L1,L2)])/(sum([x**2 for x in L1])**0.5 * sum([x**2 for x in L2])**0.5 + 10**(-16))

    def chisquareDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        s = 0.0
        for i,j in zip(l1[:length],l2[:length]):
            if i == j == 0.0:
                continue
            s += (i - j)**2 / (i + j)
        return s

    def bhattcaryyaDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        l1 = np.array(l1[:length])
        l2 = np.array(l2[:length])
        num = np.sum(np.sqrt(np.multiply(l1,l2,dtype=np.float64)),dtype=np.float64)
        den = np.sqrt(np.sum(l1,dtype=np.float64)*np.sum(l2,dtype=np.float64))
        return math.sqrt( 1 - num / den )

    def jensenDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        return sum([x*math.log(2*x/(x+y)) + y*math.log(2*y/(x+y)) for x,y in zip(l1[:length],l2[:length])])

    def bruteforcematcherDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        l1 = np.array(l1[:length]).astype('uint8')
        l2 = np.array(l2[:length]).astype('uint8')
        if l1.shape[0]==0 or l2.shape[0]==0:
            return np.inf
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = list(map(lambda x: x.distance, bf.match(l1, l2)))
        return np.mean(matches)

    def flannDistance(l1,l2): 
        length = min(len(l1),len(l2)) 
        l1 = np.float32(np.array(l1[:length]))
        l2 = np.float32(np.array(l2[:length]))
        if l1.shape[0]==0 or l2.shape[0]==0:
            return np.inf
        index_params = dict(algorithm=1, trees=5)
        sch_params = dict(checks=50)
        flannMatcher = cv2.FlannBasedMatcher(index_params, sch_params)
        matches = list(map(lambda x: x.distance, flannMatcher.match(l1, l2)))
        return np.mean(matches)
        

        
        


