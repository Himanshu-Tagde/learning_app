import random
import os
import streamlit as st

# Path to images directory
vegetable_images_path = r'E:\spacece\project 3\vegetable_images'

# List of vegetable image filenames (ensure these images exist in the folder)
vegetable_images = [
    'brinjal.jpg', 'cabbage.jpg', 'potato.jpg', 'tomato.jpg',
    'capsicum.jpg', 'onion.jpg', 'carrot.jpg', 'radish.jpg'
]

# Function to display images and ask user to count the vegetables
def count_vegetables(difficulty='easy'):
    if 'selected_images' not in st.session_state or 'options' not in st.session_state or 'correct_count' not in st.session_state:
        # If images are not in session_state, generate them now
        num_images = random.randint(1, 5) if difficulty == 'easy' else random.randint(6, 10)
        num_images = min(num_images, len(vegetable_images))  # Ensure we don't sample more than available images

        # Select random images
        selected_images = random.sample(vegetable_images, num_images)

        # Store the selected images and their count in session state
        st.session_state.selected_images = selected_images
        st.session_state.correct_count = len(selected_images)

        # Generate 4 unique options (including the correct one)
        options = {st.session_state.correct_count}
        while len(options) < 4:
            random_option = st.session_state.correct_count + random.randint(-1, 2)
            options.add(random_option)

        st.session_state.options = list(options)

    # Display the selected vegetable images in a row
    st.subheader("Guess how many vegetables you see:")
    cols = st.columns(len(st.session_state.selected_images))  # Create columns for each image
    image_paths = [os.path.join(vegetable_images_path, img) for img in st.session_state.selected_images]
    
    for i, image_path in enumerate(image_paths):
        with cols[i]:
            st.image(image_path, width=150)  # Resize each image to fit the columns

    correct_count = st.session_state.correct_count

    # Generate a unique key for the radio button based on the difficulty and selected images
    radio_key = f"radio_button_{difficulty}_{len(st.session_state.selected_images)}"

    # Display options as radio buttons for user to select
    selected_option = st.radio(
        "How many vegetables do you see in the above images?", 
        st.session_state.options, 
        key=radio_key  # Unique key for the radio button
    )

    # Handle the user's response when they click 'Submit'
    submit_key = f"submit_button_{str(st.session_state.selected_images)}_{st.session_state.correct_count}"  # Unique key for Submit button
    if st.button('Submit', key=submit_key):
        if selected_option == correct_count:
            st.success(f"Correct! There are {correct_count} vegetables!")
        else:
            st.error(f"Incorrect. There are {correct_count} vegetables. Try again!")

    # Continue button to generate a new question
    next_key = f"next_button_{str(st.session_state.selected_images)}_{st.session_state.correct_count}"  # Unique key for Next Question button
    if st.button('Next Question', key=next_key):
        # Clear the session state for a new question
        st.session_state.pop('selected_images', None)
        st.session_state.pop('options', None)
        st.session_state.pop('correct_count', None)

        # Regenerate new question
        count_vegetables(difficulty=difficulty)

# Main function to select difficulty level and start the game
def select_difficulty():
    st.markdown("""
        Welcome to the Vegetable Counting Game! 🥕🥔🍅
        Your goal is to count how many vegetables are shown in the images.
    """)

    # Add Quit button
    quit_key = "quit_button"  # Unique key for Quit button
    if st.button("Quit", key=quit_key):
        st.warning("You have exited the game. Thank you for playing!")
        st.stop()  # Stops execution of further code

    # Ensure difficulty is selected
    difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium"], key="difficulty_radio")
    count_vegetables(difficulty=difficulty.lower())

# Streamlit app execution starts here
st.title("Vegetable Counting Game")
st.markdown("### Can you count all the vegetables?")

# Run the game
select_difficulty()
