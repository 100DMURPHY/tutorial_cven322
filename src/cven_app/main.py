from nicegui import ui
import os

# Placeholder for modules
def economics_page():
    ui.label('Engineering Economics Module').classes('text-h4')
    ui.markdown('Content based on PW Analysis, Annual Analysis, B/C, and IRR.')

def optimization_page():
    ui.label('Optimization Modeling Module').classes('text-h4')
    ui.markdown('Content based on LP, IP, and NLP Formulations.')

def simulation_page():
    ui.label('Systems & Simulation Module').classes('text-h4')
    ui.markdown('Content based on Simulation and Multi-Objective Problems.')

def main():
    @ui.page('/')
    def index():
        with ui.header().classes('items-center justify-between'):
            ui.label('CVEN322: Civil Engineering Systems').classes('font-bold')
            with ui.row():
                ui.button('Economics', on_click=lambda: ui.navigate.to('/economics')).props('flat color=white')
                ui.button('Optimization', on_click=lambda: ui.navigate.to('/optimization')).props('flat color=white')
                ui.button('Simulation', on_click=lambda: ui.navigate.to('/simulation')).props('flat color=white')

        with ui.column().classes('w-full items-center p-8'):
            ui.label('Welcome to the Learning Platform').classes('text-h3 q-my-md')
            ui.markdown('''
            This platform provides interactive tools for Civil Engineering Systems analysis.
            Select a module from the header to begin.
            ''').classes('text-lg')
            
            with ui.row().classes('w-full justify-center gap-8 q-mt-xl'):
                with ui.card().classes('w-64 p-4'):
                    ui.label('Engineering Economics').classes('text-h6')
                    ui.label('Analyze project costs, benefits, and IRR.')
                    ui.button('Go', on_click=lambda: ui.navigate.to('/economics')).classes('w-full')
                
                with ui.card().classes('w-64 p-4'):
                    ui.label('Optimization').classes('text-h6')
                    ui.label('Linear and Nonlinear programming models.')
                    ui.button('Go', on_click=lambda: ui.navigate.to('/optimization')).classes('w-full')
                
                with ui.card().classes('w-64 p-4'):
                    ui.label('Systems & Sim').classes('text-h6')
                    ui.label('Simulation and Multi-Objective analysis.')
                    ui.button('Go', on_click=lambda: ui.navigate.to('/simulation')).classes('w-full')

    @ui.page('/economics')
    def econ():
        with ui.header():
            ui.button('Back', on_click=lambda: ui.navigate.to('/')).props('flat color=white icon=arrow_back')
            ui.label('Engineering Economics')
        economics_page()

    @ui.page('/optimization')
    def opt():
        with ui.header():
            ui.button('Back', on_click=lambda: ui.navigate.to('/')).props('flat color=white icon=arrow_back')
            ui.label('Optimization Modeling')
        optimization_page()

    @ui.page('/simulation')
    def sim():
        with ui.header():
            ui.button('Back', on_click=lambda: ui.navigate.to('/')).props('flat color=white icon=arrow_back')
            ui.label('Systems & Simulation')
        simulation_page()

    ui.run(title='CVEN322 Platform', port=8080, reload=False)

if __name__ in {"__main__", "builtins"}:
    main()
