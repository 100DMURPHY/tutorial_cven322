from nicegui import ui
from cven_app.modules import economics, optimization, simulation

# Global styling
def apply_theme():
    ui.colors(primary='#1e40af', secondary='#3b82f6', accent='#f59e0b')

def shared_header(title_text='CVEN322: Civil Engineering Systems', color='bg-blue-900'):
    with ui.header().classes(f'items-center justify-between px-8 {color}'):
        with ui.row().classes('items-center'):
            ui.icon('engineering', size='2rem').classes('text-white mr-2')
            if title_text == 'CVEN322: Civil Engineering Systems':
                ui.label(title_text).classes('font-bold text-xl text-white')
            else:
                ui.button(on_click=lambda: ui.navigate.to('/')).props('flat color=white icon=arrow_back')
                ui.label(title_text).classes('text-xl font-bold text-white')
        
        with ui.row().classes('gap-4 items-center'):
            ui.button('Economics', on_click=lambda: ui.navigate.to('/economics')).props('flat color=white')
            ui.button('Optimization', on_click=lambda: ui.navigate.to('/optimization')).props('flat color=white')
            ui.button('Simulation', on_click=lambda: ui.navigate.to('/simulation')).props('flat color=white')
            # Use ui.link for better reliability with external links
            with ui.element('div').classes('p-2 border border-white rounded hover:bg-white/10 transition-colors'):
                ui.link('DOCS', 'https://100dmurphy.github.io/tutorial_cven322/', new_tab=True).classes('text-white font-bold no-underline flex items-center')
                ui.icon('description', color='white').classes('ml-1')

@ui.page('/')
def index():
    apply_theme()
    shared_header()
    with ui.column().classes('w-full items-center p-12 max-w-6xl mx-auto'):
        ui.label('Advanced Engineering Systems').classes('text-h2 font-black text-blue-900 text-center')
        ui.label('Interactive Learning Platform for CVEN 322').classes('text-h5 text-gray-600 q-mb-xl text-center')
        
        ui.markdown('''
        This platform is dedicated to providing high-transparency access to core Civil Engineering systems methods.
        Explore the modules below to interact with real-world engineering concepts.
        ''').classes('text-center text-lg max-w-2xl text-gray-500 text-balance')
        
        with ui.row().classes('w-full justify-center gap-6 q-mt-xl no-wrap'):
            with ui.card().classes('w-80 p-6 hover:scale-105 transition-transform cursor-pointer shadow-xl').on('click', lambda: ui.navigate.to('/economics')):
                ui.icon('payments', size='3rem').classes('text-blue-600 q-mb-md')
                ui.label('Engineering Economics').classes('text-h5 font-bold')
                ui.label('Cash flow diagrams, time value of money, and project evaluation metrics (IRR, NPV).').classes('text-gray-500')
                ui.separator().classes('q-my-md')
                ui.button('Explore Module', icon='arrow_forward').props('flat').classes('w-full')
            
            with ui.card().classes('w-80 p-6 hover:scale-105 transition-transform cursor-pointer shadow-xl').on('click', lambda: ui.navigate.to('/optimization')):
                ui.icon('trending_up', size='3rem').classes('text-green-600 q-mb-md')
                ui.label('Optimization Modeling').classes('text-h5 font-bold')
                ui.label('Linear, Integer, and Nonlinear programming models for complex engineering decisions.').classes('text-gray-500')
                ui.separator().classes('q-my-md')
                ui.button('Explore Module', icon='arrow_forward').props('flat').classes('w-full')
            
            with ui.card().classes('w-80 p-6 hover:scale-105 transition-transform cursor-pointer shadow-xl').on('click', lambda: ui.navigate.to('/simulation')):
                ui.icon('science', size='3rem').classes('text-orange-600 q-mb-md')
                ui.label('Systems & Sim').classes('text-h5 font-bold')
                ui.label('Stochastic processes, simulation models, and multi-objective Pareto analysis.').classes('text-gray-500')
                ui.separator().classes('q-my-md')
                ui.button('Explore Module', icon='arrow_forward').props('flat').classes('w-full')

@ui.page('/economics')
def econ_page():
    apply_theme()
    shared_header('Engineering Economics', color='bg-blue-800')
    with ui.column().classes('p-8 max-w-5xl mx-auto w-full'):
        economics.content()

@ui.page('/optimization')
def opt_page():
    apply_theme()
    shared_header('Optimization Modeling', color='bg-green-800')
    with ui.column().classes('p-8 max-w-5xl mx-auto w-full'):
        optimization.content()

@ui.page('/simulation')
def sim_page():
    apply_theme()
    shared_header('Systems & Simulation', color='bg-orange-800')
    with ui.column().classes('p-8 max-w-5xl mx-auto w-full'):
        simulation.content()

def main():
    ui.run(title='CVEN322 Platform', port=8080, reload=False, dark=False)

if __name__ in {"__main__", "builtins"}:
    main()
