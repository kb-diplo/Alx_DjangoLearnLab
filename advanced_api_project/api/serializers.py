# BookSerializer: Serializes all fields of the Book model and validates the publication year.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        if value > 2023:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer: Serializes the Author model and includes nested BookSerializer for related books.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']