

def make_list_of_ids(pk):
    """
    pk: the primary key of a flashcard

    returns: a list of ids of all flashcards that are in the same set as the flashcard with given id

    Helps in finding next and previous flashcard to let the user easily browse flashcards from their set.
    """
    flashcard = Flashcard.objects.get(pk=pk)
    set = flashcard.set
    set_flashcards = Flashcard.objects.filter(set__id=set.id)
    return [f.id for f in set_flashcards]


def make_question_ids(flashcards):
    question_ids = [flashcard.pk for flashcard in flashcards]
    question_str_ids = [str(id) for id in question_ids]
    return ' '.join(question_str_ids)


def create_example_set(guest_user):
    example_set = Set.objects.create(name='example', owner=guest_user)
    examples = [('kot', 'cat'), ('pies', 'dog'), ('koń', 'horse'), ('krowa', 'cow'), ('mysz', 'mouse')]
    for example in examples:
        front = example[0]
        back = example[1]
        Flashcard.objects.create(set=example_set, owner=guest_user, front=front, back=back)