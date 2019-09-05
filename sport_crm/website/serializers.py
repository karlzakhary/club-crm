from django.conf import settings
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import fields, serializers
from collections import OrderedDict
from drf_writable_nested import WritableNestedModelSerializer
from website import models
from urllib.parse import urlparse

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'

class gTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.gTitle
        fields = '__all__'

    def to_representation(self, obj):
        return (obj.name, obj.value)

class gTextboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.gTextbox
        fields = '__all__'

    def to_representation(self, obj):
        return (obj.name, obj.value)

class ComponentSerializer(serializers.ModelSerializer):
    titles = gTitleSerializer(many=True)
    textboxs = gTextboxSerializer(many=True)
    class Meta:
        model = models.Component
        fields = ('name', 'titles', 'textboxs')

    def to_representation(self, obj):
        serialized_obj = super(ComponentSerializer, self).to_representation(obj)
        result = {}
        data = {}
        for key, value in serialized_obj["titles"]:
            data[key] = value
        for key, value in serialized_obj["textboxs"]:
            data[key] = value

        # data[slugify(title["name"])] = title["value"]

        result[serialized_obj["name"]] = data
        return (serialized_obj["name"], data)

class PageSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True)
    class Meta:
        model = models.Page
        fields = '__all__'

    def to_representation(self, obj):
        serialized_obj = super(PageSerializer, self).to_representation(obj)
        data = {}
        data["name"] = obj.name
        for key, value in serialized_obj["components"]:
            data[key] = value

        return data       

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Job

    def to_representation(self, instance):
        data = super(JobSerializer, self).to_representation(instance)
        data['responsibilities'] = data['responsibilities'].splitlines()
        data['requirements'] = data['requirements'].splitlines()
        return data

class InstagramSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Instagram

class ShowCasedProjectsListingField(serializers.RelatedField):
     def to_representation(self,value):
        result = {'id':value.id}
        return result

class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SubService

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Category

    def to_representation(self, instance):
        data = super(CategorySerializer, self).to_representation(instance)
        data['names'] = data['names'].splitlines()
        if data['image'] is not None:
            data['image'] = data['image'].replace('http://localhost:8199', '')
        return data

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Client

    def to_representation(self, instance):
        data = super(ClientSerializer, self).to_representation(instance)

        # if data['image'] is not None:
        if 'image' in data.values():
            data['image'] = data['image'].replace('http://localhost:8199', '')
        return data


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Member
    
    def to_representation(self,instance):
        data = super(MemberSerializer,self).to_representation(instance)
        if data['imageA'] is not None:
            o = urlparse(data['imageA'])
            data['imageA']= o.path
        if data['imageB'] is not None:
            o = urlparse(data['imageB'])
            data['imageB'] = o.path
        return data

class SectionASerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionA

class SectionBSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionB

class SectionCSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionC

class SectionDSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionD

class SectionESerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionE

class SectionFSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionF

class SectionGSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionG

class SectionHSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.SectionH



# class ClientListingField(serializers.RelatedField):
#     def to_representation(self,value):
#         result = {'id':value.id,
#                   'names':value.names}
#         return result 

class SmallServiceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Service
    # def to_representation(self,value):
    #     result = {'id':value.id,
    #               'title':value.title}
    #     return result

class NextProjectSerializer(serializers.RelatedField):
     def to_representation(self,value):
        result = {
                'id': value.id,
                'image': value.image
                }
        return result

class ProjectRetrieveSerializer(WritableNestedModelSerializer):
    sectiona = SectionASerializer(many=True)
    sectionb = SectionBSerializer(many=True)
    sectionc = SectionCSerializer(many=True)
    sectiond = SectionDSerializer(many=True)
    sectione = SectionESerializer(many=True)
    sectionf = SectionFSerializer(many=True)
    sectiong = SectionGSerializer(many=True)
    sectionh = SectionHSerializer(many=True)
    services = SmallServiceSerializer(many=True)
    next_project = NextProjectSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = models.Project

    def to_representation(self,obj):
        serialized_obj = super(ProjectRetrieveSerializer, self).to_representation(obj)
        data = {}
        data['name'] = obj.name
        for key,value in serialized_obj.items():
            data[key] = value

        return data

class ProjectCreateSerializer(WritableNestedModelSerializer):
    sectiona = SectionASerializer(many=True)
    sectionb = SectionBSerializer(many=True)
    sectionc = SectionCSerializer(many=True)
    sectiond = SectionDSerializer(many=True)
    sectione = SectionESerializer(many=True)
    sectionf = SectionFSerializer(many=True)
    sectiong = SectionGSerializer(many=True)
    sectionh = SectionHSerializer(many=True)
    # next_project = NextProjectSerializer(read_only=True)

    lookup_fields = ('id','slug')
    class Meta:
        fields = '__all__'
        model = models.Project

    def to_representation(self,obj):
        serialized_obj = super(ProjectCreateSerializer, self).to_representation(obj)
        data = {}
        data['name'] = obj.name
        for key,value in serialized_obj.items():
            data[key] = value

        return data

class ServiceSerializer(serializers.ModelSerializer):
    showcased_projects = ShowCasedProjectsListingField(many=True,read_only = True)
    subservices = SubServiceSerializer(many=True)
    caseStudies_projects = ProjectRetrieveSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = models.Service

    def to_representation(self,obj):
        data = super(ServiceSerializer,self).to_representation(obj)
        images_fields_names = ['image','homepage_image']
        result = {}
        for key,value in data.items():
            if key in images_fields_names:
                if value is not None:
                    o = urlparse(value)
                    value = o.path
                    value = value.replace('http://localhost:8199', '')
            result[key] = value
        return result


class LandingPageClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LandingPageClip
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Testimonial
        fields = '__all__'