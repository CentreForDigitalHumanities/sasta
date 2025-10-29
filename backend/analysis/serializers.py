from rest_framework import serializers
from .models import (AnalysisRun, AssessmentMethod, AssessmentQuery, Corpus,
                     MethodCategory, Transcript, UploadFile, Utterance)


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['name', 'content', 'status', 'corpus']


class AnalysisRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisRun
        fields = ('id', 'created', 'annotation_file', 'method', 'is_manual_correction')


class UtteranceSerializer(serializers.ModelSerializer):
    for_analysis = serializers.ReadOnlyField()

    class Meta:
        model = Utterance
        fields = ('id', 'sentence', 'speaker', 'utt_id', 'uttno', 'xsid', 'for_analysis', 'parse_tree')


class TranscriptListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='get_status_display')

    class Meta:
        model = Transcript
        fields = ('id', 'name', 'status', 'status_name', 'date_added', 'utterances', 'corpus')


class TranscriptDetailsSerializer(serializers.ModelSerializer):
    def get_latest_run(self, obj):
        try:
            latest = obj.analysisruns.latest()
            return AnalysisRunSerializer(latest).data
        except AnalysisRun.DoesNotExist:
            return None

    def get_latest_corrections(self, obj):
        try:
            latest = obj.analysisruns.filter(is_manual_correction=True).latest()
            return AnalysisRunSerializer(latest).data
        except AnalysisRun.DoesNotExist:
            return None

    latest_run = serializers.SerializerMethodField()
    latest_corrections = serializers.SerializerMethodField()
    status = serializers.ChoiceField(choices=Transcript.STATUS_CHOICES)
    status_name = serializers.CharField(source='get_status_display')
    utterances = UtteranceSerializer(read_only=True, many=True)

    class Meta:
        model = Transcript
        fields = ('id', 'name', 'content',
                  'parsed_content', 'corrected_content', 'status', 'status_name', 'date_added',
                  'corpus', 'utterances', 'latest_run', 'latest_corrections', 'target_speakers')


class CorpusListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    num_transcripts = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username", read_only=True)

    def get_num_transcripts(self, obj):
        return obj.transcripts.count()

    class Meta:
        model = Corpus
        fields = ('id', 'name', 'method_category', 'num_transcripts', 'username')


class CorpusDetailsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    transcripts = TranscriptListSerializer(read_only=True, many=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Corpus
        fields = ('id', 'name', 'status', 'default_method', 'method_category',
                  'date_added', 'date_modified', 'transcripts', 'username', 'share_permission')


class AssessmentQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentQuery
        fields = '__all__'


class MethodCategorySerializer(serializers.ModelSerializer):
    has_form = serializers.BooleanField()
    variants = serializers.SerializerMethodField()

    class Meta:
        model = MethodCategory
        fields = ('id', 'name', 'zc_embeddings',
                  'levels', 'has_form', 'variants')

    def get_variants(self, obj):
        # TODO: implement with actual variants
        known_variants = {}
        cat_variants = known_variants.get(obj.name.lower(), None)
        if cat_variants:
            return [{'key': v.get('key'), 'label': v.get('label')} for v in cat_variants]
        return []


class AssessmentMethodSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    queries = AssessmentQuerySerializer(read_only=True, many=True)
    date_added = serializers.DateField(format='%d-%m-%Y', read_only=True)
    category = MethodCategorySerializer()

    class Meta:
        model = AssessmentMethod
        fields = ('id', 'name', 'category', 'content',
                  'date_added', 'queries', )
