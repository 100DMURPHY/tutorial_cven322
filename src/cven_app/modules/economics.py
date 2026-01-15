from nicegui import ui
import numpy as np

def content():
    ui.label('Engineering Economics').classes('text-h3 q-my-md')
    ui.markdown('''
    Engineering economics involves the systematic evaluation of the economic merits of proposed solutions to engineering problems.
    
    ### Key Concept: Time Value of Money
    Money has a time value because it can be invested and earn interest. Concepts like **Present Worth (P)**, **Future Worth (F)**, and **Uniform Series (A)** are fundamental.
    ''').classes('text-lg')

    with ui.tabs().classes('w-full') as tabs:
        t1 = ui.tab('Single Payment (P/F)')
        t2 = ui.tab('Uniform Series (P/A)')
        t3 = ui.tab('Project Comparison (PW)')

    with ui.tab_panels(tabs, value=t1).classes('w-full bg-transparent'):
        with ui.tab_panel(t1):
            single_payment_calculator()
        with ui.tab_panel(t2):
            uniform_series_calculator()
        with ui.tab_panel(t3):
            project_comparison_module()

def single_payment_calculator():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Single Payment: Future Value (F) from Present Value (P)').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('flex-1'):
                p_slider = ui.slider(min=0, max=10000, value=1000).props('label-always')
                ui.label('Present Value (P): $').bind_text_from(p_slider, 'value', backward=lambda v: f'{v:,.0f}')
                
                rate_slider = ui.slider(min=0, max=20, value=5, step=0.1).props('label-always')
                ui.label('Interest Rate (i): %').bind_text_from(rate_slider, 'value', backward=lambda v: f'{v:.1f}')
                
                years_slider = ui.slider(min=1, max=30, value=10).props('label-always')
                ui.label('Years (n): ').bind_text_from(years_slider, 'value')

            with ui.column().classes('flex-1 items-center justify-center bg-blue-50 rounded-lg p-4'):
                result_label = ui.label('').classes('text-h4 text-blue-800 font-bold')
                ui.label('Future Value (F)').classes('text-subtitle1 text-blue-600')

                def update():
                    p = p_slider.value
                    i = rate_slider.value / 100
                    n = years_slider.value
                    f = p * ((1 + i) ** n)
                    result_label.text = f'${f:,.2f}'
                    chart.options['series'][0]['data'] = [p * ((1 + i)**year) for year in range(int(n) + 1)]
                    chart.update()

                p_slider.on('update:model-value', update)
                rate_slider.on('update:model-value', update)
                years_slider.on('update:model-value', update)

        chart = ui.echart({
            'xAxis': {'type': 'category', 'data': [str(y) for y in range(31)], 'name': 'Year'},
            'yAxis': {'type': 'value', 'name': 'Value ($)'},
            'tooltip': {'trigger': 'axis'},
            'series': [{
                'data': [],
                'type': 'line',
                'smooth': True,
                'areaStyle': {'color': 'rgba(59, 130, 246, 0.2)'},
                'lineStyle': {'color': '#3b82f6', 'width': 3}
            }]
        }).classes('w-full h-64 q-mt-md')
        update()

def uniform_series_calculator():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Uniform Series: Present Value (P) from Annual Amount (A)').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('flex-1'):
                a_slider = ui.slider(min=0, max=1000, value=100).props('label-always')
                ui.label('Annual Payment (A): $').bind_text_from(a_slider, 'value', backward=lambda v: f'{v:,.0f}')
                
                rate_slider = ui.slider(min=0, max=20, value=5, step=0.1).props('label-always')
                ui.label('Interest Rate (i): %').bind_text_from(rate_slider, 'value', backward=lambda v: f'{v:.1f}')
                
                years_slider = ui.slider(min=1, max=30, value=10).props('label-always')
                ui.label('Years (n): ').bind_text_from(years_slider, 'value')

            with ui.column().classes('flex-1 items-center justify-center bg-green-50 rounded-lg p-4'):
                result_label = ui.label('').classes('text-h4 text-green-800 font-bold')
                ui.label('Equivalent Present Value (P)').classes('text-subtitle1 text-green-600')

                def update():
                    a = a_slider.value
                    i = rate_slider.value / 100
                    n = years_slider.value
                    if i == 0:
                        p = a * n
                    else:
                        p = a * (((1 + i)**n - 1) / (i * (1 + i)**n))
                    result_label.text = f'${p:,.2f}'
                    
                    # Cumulative value visualization
                    chart.options['series'][0]['data'] = [a * (((1 + i)**y - 1) / (i * (1 + i)**y)) if i > 0 else a * y for y in range(int(n) + 1)]
                    chart.update()

                a_slider.on('update:model-value', update)
                rate_slider.on('update:model-value', update)
                years_slider.on('update:model-value', update)

        chart = ui.echart({
            'xAxis': {'type': 'category', 'data': [str(y) for y in range(31)], 'name': 'Year'},
            'yAxis': {'type': 'value', 'name': 'Present Value ($)'},
            'series': [{
                'data': [],
                'type': 'bar',
                'itemStyle': {'color': '#10b981'}
            }]
        }).classes('w-full h-64 q-mt-md')
        update()

def project_comparison_module():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Project Comparison: PW Analysis').classes('text-h5 q-mb-md')
        ui.markdown('Compare two projects with different cash flows over the same period.')
        
        with ui.row().classes('w-full gap-4'):
            rate = ui.number('Discount Rate (%)', value=10, format='%.1f').classes('w-32')
            years = ui.number('Life Span (Years)', value=5, precision=0).classes('w-32')

        with ui.row().classes('w-full gap-8 q-mt-md'):
            with ui.column().classes('flex-1 p-4 bg-gray-50 rounded'):
                ui.label('Project A').classes('font-bold border-b w-full mb-2')
                cost_a = ui.number('Initial Cost ($)', value=5000)
                benefit_a = ui.number('Annual Benefit ($)', value=1500)
            
            with ui.column().classes('flex-1 p-4 bg-gray-50 rounded'):
                ui.label('Project B').classes('font-bold border-b w-full mb-2')
                cost_b = ui.number('Initial Cost ($)', value=8000)
                benefit_b = ui.number('Annual Benefit ($)', value=2200)

        def calculate_pw():
            i = rate.value / 100
            n = int(years.value)
            factor = (((1 + i)**n - 1) / (i * (1 + i)**n)) if i > 0 else n
            pw_a = -cost_a.value + benefit_a.value * factor
            pw_b = -cost_b.value + benefit_b.value * factor
            
            chart.options['series'][0]['data'] = [round(pw_a, 2), round(pw_b, 2)]
            chart.update()
            
            verdict.text = f'Project {"B" if pw_b > pw_a else "A"} is better by PW analysis.'
            verdict.classes('text-green-600' if (pw_b > pw_a if pw_b > 0 else pw_a > 0) else 'text-red-400')

        button = ui.button('Calculate & Compare', on_click=calculate_pw).classes('w-full q-mt-md')
        
        chart = ui.echart({
            'xAxis': {'type': 'category', 'data': ['Project A', 'Project B']},
            'yAxis': {'type': 'value', 'name': 'Net Present Worth ($)'},
            'series': [{'data': [0, 0], 'type': 'bar'}]
        }).classes('w-full h-48 q-mt-md')
        
        verdict = ui.label('').classes('text-xl font-bold text-center w-full q-mt-md')
