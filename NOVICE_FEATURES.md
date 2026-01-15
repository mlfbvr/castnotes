# CastNotes: Required Features for a Novice Angler's Web App

## Application Type & Core Purpose
A responsive, mobile-first web application designed to let you quickly and easily record the details of every fish you catch.

## Key Technologies
*   **Frontend:** A beautiful and modern React single-page application, styled with Bootstrap and adhering to Material Design principles for a clean and intuitive user experience.
*   **Backend:** A robust backend powered by the Django framework.
*   **Database:** A powerful and scalable PostgreSQL database.

## Main Features & User Interaction
1.  **Log a New Catch:** A prominent "Add Catch" button will open a simple form where you can record:
    *   **Fish Species:** An easy-to-use search with auto-complete, potentially with images to help identification.
    *   **Photo:** Upload a picture of your catch.
    *   **Location:** Automatically captured using your device's GPS, and displayed on an interactive map. You can also drop a pin manually.
    *   **Date & Time:** Automatically pre-filled.
    *   **Weather (Optional):** Basic weather conditions (e.g., sunny, cloudy, rainy) can be noted.
    *   **Notes (Optional):** A simple text area for any extra details, like the lure you used or the fight it put up.

2.  **My Catches:** A gallery view of all your past catches, with the most recent first. Each entry will show the fish photo, species, and date. Clicking a catch will take you to a detailed view.

3.  **Catch Map:** A full-screen map showing pins for all your catch locations. Clicking a pin will show a quick summary of the catch.

## Visual Design & User Experience (UX)
The app will have a clean and modern design with a nature-inspired color palette (blues, greens, and earthy tones). The focus will be on an intuitive, "thumb-friendly" interface that you can use with one hand while holding your fishing rod in the other. All interactions will be designed to be quick and seamless, so you can get back to fishing.
