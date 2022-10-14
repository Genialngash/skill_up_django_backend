# class JobCategoriesView(viewsets.ViewSet):
#     serializer_class = JobCategorySerializer

#     def get_queryset(self):
#         queryset = JobCategory.objects.all()
#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = JobCategorySerializer(queryset, many=True)
#         return Response({
#             'data': serializer.data,
#             'status': 'ok',
#             'status_code': 200,
#             'message': 'Success.',
#         })

#     def perform_create(self, serializer):
#         serializer.save()

#     def create(self, request, *args, **kwargs):
#         serializer = JobCategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response({
#             'data': serializer.data,
#             'status': 'ok',
#             'message': 'Category created successfully.',
#             'status_code': 201,

#         }, status=status.HTTP_201_CREATED)

#     def perform_update(self, serializer):
#         serializer.save()


#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)

#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}

#         return Response({
#             'data': serializer.data,
#             'status': 'ok',
#             'message': 'Category updated successfully.',
#             'status_code': 200,
#         })

