import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Score
        self.score = 0
        self.total_attempts = 0

        # Feedback
        self.feedback_msg = "Solve the card and press Enter!"
        self.feedback_color = (200, 205, 215)

        # Question
        self.num_a = 0
        self.num_b = 0
        self.operator = "+"

        # --------------------------------
        # Task 2: Countdown Timer
        # --------------------------------
        self.timer_duration = 10.0
        self.time_left = self.timer_duration
        self.timer_start = pygame.time.get_ticks()

        # --------------------------------
        # Task 3: Streak Multiplier
        # --------------------------------
        self.streak = 0
        self.multiplier = 1

        # --------------------------------
        # Input Box
        # --------------------------------
        box_w, box_h = 130, 44

        self.input_box = TextBox(
            width // 2 - 110,
            230,
            box_w,
            box_h
        )

        # --------------------------------
        # Submit Button
        # --------------------------------
        self.submit_btn = pygame.Rect(
            width // 2 + 30,
            230,
            90,
            box_h
        )

        # --------------------------------
        # Fonts
        # --------------------------------
        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_card = pygame.font.SysFont(None, 56)
        self.font_btn = pygame.font.SysFont(None, 24)

        # Create first question
        self.generate_new_card()

    # ==========================================
    # Generate New Question
    # ==========================================
    def generate_new_card(self):

        # Task 4: Add integer division
        self.operator = random.choice(
            ["+", "-", "*", "/"]
        )

        if self.operator == "/":

            # Generate divisor
            self.num_b = random.randint(2, 12)

            # Generate quotient
            quotient = random.randint(1, 12)

            # Generate dividend
            # This guarantees a whole-number answer.
            self.num_a = self.num_b * quotient

        else:

            self.num_a = random.randint(3, 15)
            self.num_b = random.randint(2, 12)

            # Keep subtraction non-negative
            if (
                self.operator == "-"
                and self.num_a < self.num_b
            ):
                self.num_a, self.num_b = (
                    self.num_b,
                    self.num_a
                )

        # Clear old answer
        self.input_box.clear()

        # Restart timer
        self.time_left = self.timer_duration
        self.timer_start = pygame.time.get_ticks()

    # ==========================================
    # Calculate Correct Answer
    # ==========================================
    def compute_expected_answer(self):

        # Task 1: Correct arithmetic calculation

        if self.operator == "+":
            return self.num_a + self.num_b

        elif self.operator == "-":
            return self.num_a - self.num_b

        elif self.operator == "*":
            return self.num_a * self.num_b

        # Task 4: Integer division
        elif self.operator == "/":
            return self.num_a // self.num_b

    # ==========================================
    # Submit Answer
    # ==========================================
    def submit_answer(self):

        val_str = self.input_box.text.strip()

        # Empty input does not count as an attempt
        if not val_str or val_str == "-":

            self.feedback_msg = "Type an answer first!"
            self.feedback_color = (240, 175, 40)

            return

        user_answer = int(val_str)

        expected = self.compute_expected_answer()

        self.total_attempts += 1

        # --------------------------------
        # Correct Answer
        # --------------------------------
        if user_answer == expected:

            # Increase streak
            self.streak += 1

            # Apply multiplier
            if self.streak >= 5:
                self.multiplier = 3

            elif self.streak >= 3:
                self.multiplier = 2

            else:
                self.multiplier = 1

            # Add score
            self.score += self.multiplier

            # Short feedback so it fits on screen
            self.feedback_msg = (
                f"CORRECT! Answer = {expected}"
            )

            self.feedback_color = (80, 230, 110)

            # Generate next question
            self.generate_new_card()

        # --------------------------------
        # Wrong Answer
        # --------------------------------
        else:

            # Reset streak
            self.streak = 0
            self.multiplier = 1

            self.feedback_msg = (
                f"WRONG! Expected {expected}"
            )

            self.feedback_color = (240, 75, 75)

            # Clear input
            self.input_box.clear()

    # ==========================================
    # Handle Keyboard / Mouse Events
    # ==========================================
    def handle_event(self, event):

        self.input_box.handle_event(event)

        # Press Enter
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_RETURN
        ):
            self.submit_answer()

        # Click Submit
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            if self.submit_btn.collidepoint(event.pos):
                self.submit_answer()

    # ==========================================
    # Update Timer
    # ==========================================
    def update(self):

        # Calculate elapsed time
        elapsed = (
            pygame.time.get_ticks()
            - self.timer_start
        ) / 1000.0

        # Calculate remaining time
        self.time_left = max(
            0.0,
            self.timer_duration - elapsed
        )

        # --------------------------------
        # Time Expired
        # --------------------------------
        if self.time_left <= 0.0:

            self.total_attempts += 1

            # Reset streak
            self.streak = 0
            self.multiplier = 1

            self.feedback_msg = "TIME'S UP!"
            self.feedback_color = (240, 75, 75)

            # Move to next question
            self.generate_new_card()

    # ==========================================
    # Render Game
    # ==========================================
    def render(self, screen):

        # Background
        screen.fill((25, 29, 37))

        # ======================================
        # TITLE
        # ======================================
        title_surf = self.font_title.render(
            "Math Flashcards Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                18
            )
        )

        # ======================================
        # SCORE
        # ======================================
        score_surf = self.font_hud.render(
            f"Score: {self.score} / {self.total_attempts}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2
                - score_surf.get_width() // 2,
                58
            )
        )

        # ======================================
        # STREAK + MULTIPLIER
        # ======================================
        streak_surf = self.font_hud.render(
            f"Streak: {self.streak}    "
            f"Multiplier: {self.multiplier}x",
            True,
            (245, 245, 245)
        )

        screen.blit(
            streak_surf,
            (
                self.width // 2
                - streak_surf.get_width() // 2,
                78
            )
        )

        # ======================================
        # QUESTION CARD
        # ======================================
        card_rect = pygame.Rect(
            self.width // 2 - 130,
            105,
            260,
            100
        )

        pygame.draw.rect(
            screen,
            (240, 242, 245),
            card_rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (85, 120, 175),
            card_rect,
            width=3,
            border_radius=12
        )

        card_str = (
            f"{self.num_a} "
            f"{self.operator} "
            f"{self.num_b}"
        )

        card_surf = self.font_card.render(
            card_str,
            True,
            (25, 30, 42)
        )

        screen.blit(
            card_surf,
            (
                card_rect.centerx
                - card_surf.get_width() // 2,
                card_rect.centery
                - card_surf.get_height() // 2
            )
        )

        # ======================================
        # ANSWER INPUT
        # ======================================
        self.input_box.render(screen)

        # ======================================
        # TIMER
        # ======================================

        timer_x = self.width // 2 - 130
        timer_y = 280
        timer_w = 260
        timer_h = 22

        # Black background
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (
                timer_x,
                timer_y,
                timer_w,
                timer_h
            ),
            border_radius=6
        )

        # White border
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                timer_x,
                timer_y,
                timer_w,
                timer_h
            ),
            width=2,
            border_radius=6
        )

        # Remaining time width
        progress_w = int(
            timer_w
            * (
                self.time_left
                / self.timer_duration
            )
        )

        if progress_w > 0:

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (
                    timer_x,
                    timer_y,
                    progress_w,
                    timer_h
                ),
                border_radius=5
            )

        # Countdown text
        timer_txt = self.font_btn.render(
            f"TIME: {self.time_left:.1f} s",
            True,
            (255, 255, 255)
        )

        screen.blit(
            timer_txt,
            (
                self.width // 2
                - timer_txt.get_width() // 2,
                timer_y + 28
            )
        )

        # ======================================
        # SUBMIT BUTTON
        # ======================================
        pygame.draw.rect(
            screen,
            (45, 140, 80),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (215, 225, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_txt = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_txt,
            (
                self.submit_btn.centerx
                - btn_txt.get_width() // 2,
                self.submit_btn.centery
                - btn_txt.get_height() // 2
            )
        )

        # ======================================
        # FEEDBACK
        # ======================================

        # Smaller font prevents text from being cut off
        feedback_font = pygame.font.SysFont(
            None,
            22
        )

        msg_surf = feedback_font.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        # If message is still too wide,
        # reduce font size.
        max_feedback_width = self.width - 40

        if msg_surf.get_width() > max_feedback_width:

            feedback_font = pygame.font.SysFont(
                None,
                18
            )

            msg_surf = feedback_font.render(
                self.feedback_msg,
                True,
                self.feedback_color
            )

        screen.blit(
            msg_surf,
            (
                self.width // 2
                - msg_surf.get_width() // 2,
                350
            )
        )