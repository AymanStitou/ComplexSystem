from flock import Flock
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, NUM_BOIDS, DEFAULTS
from ui import Panel, DigitInputBox, TextUI, SemiCirclePanel, Button, IntegerInputBox
import pygame
from LivePlot import LivePlot, LivePlotNeighbours
bg = pygame.image.load("stockimage_sky.jpg")

def update_ui_layout(screen_width, screen_height):
    panel = Panel(0, 0, screen_width, 2*screen_height / 3, color=(255,255,255))
    sub_panel = Panel(3.2* screen_width/5, 0.1*screen_height, 1.7*screen_width/5, screen_height / 3, color=(255,255,255), border_color=(0,0,0), border_width=3)
    separation_input = DigitInputBox(1 * screen_width / 7, 0.3*screen_height/9, screen_width/12, screen_height/20, initial_value=1.00, screen_width=screen_width, screen_height=screen_height)
    alignment_input = DigitInputBox(1 * screen_width / 7, 1.3*screen_height/9, screen_width/12, screen_height/20, initial_value=1.00, screen_width=screen_width, screen_height=screen_height)
    cohesion_input = DigitInputBox(1 * screen_width / 7, 2.3*screen_height/9, screen_width/12, screen_height/20, initial_value=1.00, screen_width=screen_width, screen_height=screen_height)
    max_speed_input = DigitInputBox(1 * screen_width / 7, 3.3*screen_height/9, screen_width/12, screen_height/20, initial_value=5.00, min_value=0.10, max_value=99.99, screen_width=screen_width, screen_height=screen_height)
    perception_radius_input = DigitInputBox(1 * screen_width / 7, 4.3*screen_height/9, screen_width/12, screen_height/20, initial_value=50.00, min_value=1.00, max_value=99.99, screen_width=screen_width, screen_height=screen_height)
    
    instructions_label = TextUI("INSTRUCTIONS", 3.64 * screen_width/5, 0.04 * screen_height, font_size=int(25*screen_height/SCREEN_HEIGHT))
    separation_label = TextUI("Separation:", 0.1 * screen_width / 5, 0.4*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    alignment_label = TextUI("Alignment:", 0.1 * screen_width / 5, 1.4*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    cohesion_label = TextUI("Cohesion:", 0.1 * screen_width / 5, 2.4*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    max_speed_label = TextUI("Max Speed:", 0.1 * screen_width / 5, 3.4*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    perception_label = TextUI("Perception", 0.1 * screen_width / 5, 4.3*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    radius_label = TextUI("Radius:", 0.16 * screen_width / 5, 4.53*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    total_label = TextUI("Total", 0.16 * screen_width / 5, 5.3*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))   
    boids_label = TextUI("Boids:", 0.16 * screen_width / 5, 5.53*screen_height/9, font_size=int(20*screen_height/SCREEN_HEIGHT))
    menu_panel = SemiCirclePanel(x=screen_width // 2, y=0, radius=3*screen_width/37, color=(200, 0, 0))

    reset_button = Button(
    x=0.65*screen_width,  
    y=panel.height-0.1*screen_height,  
    width=0.1*screen_width,
    height=0.05*screen_height,
    text="Reset",
    font_size=int(30 * screen_height/SCREEN_HEIGHT),
    tooltip_text=" Reset the simulation",
    screen_width=screen_width,
    screen_height=screen_height
    )

    perception_circle_button = Button(
    x=0.8*screen_width,
    y=panel.height-0.1*screen_height,
    width=0.16*screen_width, 
    height=0.05*screen_height,
    text="Show Perception",
    font_size=int(30 * screen_height/SCREEN_HEIGHT),
    tooltip_text="Show the perception range of a boid",
    screen_width=screen_width,
    screen_height=screen_height
    )
    
    boid_count_input = IntegerInputBox(
    x=1 * screen_width / 7,
    y=5.3*screen_height/9,
    width=screen_width/12,
    height=screen_height/20,
    initial_value=100,
    min_value=1,
    max_value=300,
    screen_width=screen_width,
    screen_height=screen_height
    )
    

    return {
        "panel": panel,
        "sub_panel": sub_panel,
        "separation_input": separation_input,
        "alignment_input": alignment_input,
        "cohesion_input": cohesion_input,
        "max_speed_input": max_speed_input,
        "perception_radius_input": perception_radius_input,
        "separation_label": separation_label,
        "alignment_label": alignment_label,
        "cohesion_label": cohesion_label,
        "max_speed_label": max_speed_label,
        "perception_label": perception_label,
        "radius_label": radius_label,
        "total_label": total_label,
        "boids_label": boids_label,
        "instructions_label": instructions_label,
        "menu_panel": menu_panel,
        "reset_button": reset_button,
        "perception_circle_button": perception_circle_button,
        "boid_count_input": boid_count_input
    }



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()

    # Initialize flock and UI components
    screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
    flock = Flock(NUM_BOIDS, screen_width, screen_height)
    ui_elements = update_ui_layout(screen_width, screen_height)

    # Initialize live plot
    live_plot = LivePlot(x=1.8*screen_width/5, y=0.5*screen_height/9, width=screen_width/4, height=screen_height/5, max_points=100,min_y_scale=1)
    # Initialize live plot for neighbors
    live_plot_neighbors = LivePlotNeighbours(x=live_plot.x, y=live_plot.y+1.7*live_plot.height, width=screen_width/4, height=screen_height/5, max_points=100, min_y_scale=3
                                         )
    running = True
    hideUI = True
    show_radius = False

    while running:
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update screen dimensions and UI layout on resize
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                flock = Flock(NUM_BOIDS, screen_width, screen_height)
                ui_elements = update_ui_layout(screen_width, screen_height)
                ui_elements["menu_panel"].screen_height = screen_height

                # Initialize live plot
                live_plot = LivePlot(x=1.8*screen_width/5, y=0.5*screen_height/9, width=screen_width/4, height=screen_height/5, max_points=100,min_y_scale=1)
                # Initialize live plot for neighbors
                live_plot_neighbors = LivePlotNeighbours(x=live_plot.x, y=live_plot.y+1.7*live_plot.height, width=screen_width/4, height=screen_height/5, max_points=100, min_y_scale=3)
                # Update live plots with new screen height
                live_plot.set_screen_height(screen_height)
                live_plot_neighbors.set_screen_height(screen_height)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui_elements["menu_panel"].is_clicked(event.pos):  # Detect click on semicircle
                    hideUI = not hideUI
            if event.type == pygame.KEYUP:
                # if event.key == pygame.K_BACKSPACE:
                #     backSpace = True
                if (event.key == pygame.K_m or event.key == pygame.K_SPACE) or event.key == pygame.K_ESCAPE:
                    hideUI = not hideUI
            if not hideUI:
            # Handle input box events
                ui_elements["separation_input"].handle_event(event)
                ui_elements["alignment_input"].handle_event(event)
                ui_elements["cohesion_input"].handle_event(event)
                ui_elements["max_speed_input"].handle_event(event)
                ui_elements["perception_radius_input"].handle_event(event)
                ui_elements["boid_count_input"].handle_event(event)
                ui_elements["reset_button"].handle_event(event)
                ui_elements["perception_circle_button"].handle_event(event)
                # Retrieve the number of boids from the input box
                new_boid_count = ui_elements["boid_count_input"].get_value()

                # Check if the number of boids has changed
                if len(flock.boids) != new_boid_count:
                    flock = Flock(new_boid_count, screen_width, screen_height)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ui_elements["reset_button"].is_clicked(event.pos):
                        # Reset UI inputs to default values
                        ui_elements["separation_input"].value = DEFAULTS["separation"]
                        ui_elements["separation_input"].text = f"{DEFAULTS['separation']:.2f}"

                        ui_elements["alignment_input"].value = DEFAULTS["alignment"]
                        ui_elements["alignment_input"].text = f"{DEFAULTS['alignment']:.2f}"

                        ui_elements["cohesion_input"].value = DEFAULTS["cohesion"]
                        ui_elements["cohesion_input"].text = f"{DEFAULTS['cohesion']:.2f}"

                        ui_elements["max_speed_input"].value = DEFAULTS["max_speed"]
                        ui_elements["max_speed_input"].text = f"{DEFAULTS['max_speed']:.2f}"

                        ui_elements["perception_radius_input"].value = DEFAULTS["perception_radius"]
                        ui_elements["perception_radius_input"].text = f"{DEFAULTS['perception_radius']:.2f}"

                        ui_elements["boid_count_input"].value = DEFAULTS["number_boids"]
                        ui_elements["boid_count_input"].text = f"{DEFAULTS['number_boids']}"

                        show_radius = DEFAULTS["show_perception"]
                        # Reset flock
                        flock = Flock(NUM_BOIDS, screen_width, screen_height)
                    if ui_elements["perception_circle_button"].is_clicked(event.pos):
                        show_radius = not show_radius

        # Get input box values
        separation_weight = ui_elements["separation_input"].get_value()
        alignment_weight = ui_elements["alignment_input"].get_value()
        cohesion_weight = ui_elements["cohesion_input"].get_value()
        max_speed = ui_elements["max_speed_input"].get_value()
        perception_radius = ui_elements["perception_radius_input"].get_value()

        # Update flock with weights
        flock.apply_rules(separation_weight, alignment_weight, cohesion_weight, perception_radius, max_speed)
        flock.update(max_speed)
        flock.draw(screen)

        if show_radius and len(flock.boids) > 0:
            flock.boids[0].draw_perception_radius(screen, ui_elements["perception_radius_input"].get_value())

        if  len(flock.boids) > 0:
            avg_velocity = sum(boid.velocity.length() for boid in flock.boids) / len(flock.boids)
            live_plot.add_data(avg_velocity, max_speed)
            avg_neighbors = sum(len(boid.get_neighbours(flock.boids, perception_radius)) for boid in flock.boids) / len(flock.boids)
            max_neighbours = len(flock.boids) - 1  # Theoretical max neighbors
            live_plot_neighbors.add_data(avg_neighbors, max_neighbours)

        if hideUI:
            # Render the semicircular menu
            ui_elements["menu_panel"].y =0
            ui_elements["menu_panel"].render(screen)
        else:
            # Render the panel and input boxes
            ui_elements["menu_panel"].y = ui_elements["panel"].height
            ui_elements["menu_panel"].render(screen)

            ui_elements["panel"].Render(screen)
            ui_elements["sub_panel"].Render(screen)
            ui_elements["separation_label"].render(screen)
            ui_elements["alignment_label"].render(screen)
            ui_elements["cohesion_label"].render(screen)
            ui_elements["max_speed_label"].render(screen)
            ui_elements["perception_label"].render(screen)
            ui_elements["radius_label"].render(screen)
            ui_elements["total_label"].render(screen)
            ui_elements["boids_label"].render(screen)
            ui_elements["instructions_label"].render(screen)
            ui_elements["separation_input"].render(screen)
            ui_elements["alignment_input"].render(screen)
            ui_elements["cohesion_input"].render(screen)
            ui_elements["max_speed_input"].render(screen)
            ui_elements["perception_radius_input"].render(screen)
            ui_elements["reset_button"].render(screen)
            ui_elements["perception_circle_button"].render(screen)
            ui_elements["boid_count_input"].render(screen)

            # Render live plot
            
            live_plot.render(screen)
            live_plot_neighbors.render(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()