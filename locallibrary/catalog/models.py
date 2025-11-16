from django.db import models


class Author(models.Model):
    """Autor de un libro."""
    first_name = models.CharField("Nombre", max_length=100)
    last_name = models.CharField("Apellido", max_length=100)

    def __str__(self):
        # Cómo se muestra el autor en el admin y en la consola
        return f"{self.last_name}, {self.first_name}"


class Genre(models.Model):
    """Género del libro (terror, drama, etc.)."""
    name = models.CharField("Nombre del género", max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """Libro (título + autor + géneros)."""
    title = models.CharField("Título", max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Autor del libro",
    )
    # Un libro puede tener varios géneros, y un género puede pertenecer a varios libros
    genres = models.ManyToManyField(
        Genre,
        blank=True,
        help_text="Seleccioná uno o más géneros",
    )

    def __str__(self):
        return self.title


class BookInstance(models.Model):
    """
    Ejemplar físico de un libro.
    Por ejemplo: 3 copias del mismo libro en la biblioteca.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # Estado muy simple para no complicar
    STATUS_CHOICES = [
        ("D", "Disponible"),
        ("P", "Prestado"),
    ]
    status = models.CharField(
        "Estado",
        max_length=1,
        choices=STATUS_CHOICES,
        default="D",
    )

    def __str__(self):
        # Ej: "Copia de El principito (Disponible)"
        return f"Copia de {self.book.title} ({self.get_status_display()})"
