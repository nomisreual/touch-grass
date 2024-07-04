from ninja import ModelSchema

from main.models import Post


class PostOutSchema(ModelSchema):
	class Meta:
		model = Post
		fields = ["title", "content"]
