import nltk
from nltk.corpus import wordnet


def get_lesson_with_highest_semantic_score(tags, lessons):
    max_score = -1
    best_lesson = None

    # Calculate the semantic score for each lesson
    for lesson in lessons:
        lesson = lesson["relevant_subjects"]["topic"]
        score = 0
        for tag in tags:
            # get the first synset for the tag
            tag_synset = wordnet.synsets(tag)[0]
            # get the synsets for each word in the lesson
            lesson_synsets = [wordnet.synsets(word) for word in lesson["tags"]]
            # flatten the list of synsets
            lesson_synsets = [
                synset for synsets in lesson_synsets for synset in synsets]
            # Calculate the similarity between the tag and each word in the lesson
            similarities = [tag_synset.path_similarity(
                lesson_synset) for lesson_synset in lesson_synsets]
            # get the highest similarity, or 0 if no similarities were found
            max_similarity = max(similarities) if any(similarities) else 0
            #score += max_similarity
            if score < max_similarity:
                score = max_similarity
        # Update the best lesson if this one has a higher score
        if score > max_score:
            max_score = score
            best_lesson = lesson

    return best_lesson


def main():
    lessons = [{'name': 'Lesson 1', 'tags': ['math', 'algebra', 'equations', 'functions']},
               {'name': 'Lesson 2', 'tags': [
                   'science', 'chemistry', 'atoms', 'molecules']},
               {'name': 'Lesson 3', 'tags': [
                   'history', 'civilization', 'ancient', 'rome']},
               {'name': 'Lesson 4', 'tags': [
                   'literature', 'poetry', 'shakespeare', 'sonnets']}
               ]

    lesson_tags = ['poems']

    suitable_lessons = get_lesson_with_highest_semantic_score(
        lesson_tags, lessons)

    print(suitable_lessons)


if __name__ == "__main__":
    main()
