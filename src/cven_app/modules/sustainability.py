from nicegui import ui
import numpy as np

def content():
    ui.label('Sustainability in Engineering').classes('text-h3 q-my-md')
    ui.markdown('''
    Sustainability is the ability to meet the needs of the present without compromising the ability of future generations to meet their own needs.
    In Civil Engineering, this means balancing economic growth, environmental protection, and social equity.
    ''').classes('text-lg')

    with ui.tabs().classes('w-full') as tabs:
        t1 = ui.tab('Pillars of Sustainability')
        t2 = ui.tab('Weak vs. Strong Sustainability')
        t3 = ui.tab('Project Carbon Calculator')

    with ui.tab_panels(tabs, value=t1).classes('w-full bg-transparent'):
        with ui.tab_panel(t1):
            pillars_tool()
        with ui.tab_panel(t2):
            sustainability_theory_tool()
        with ui.tab_panel(t3):
            carbon_calculator_tool()

def pillars_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('The Three Pillars: Economic, Social, and Environmental').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full justify-center items-center gap-12'):
            # Interactive Venn Diagram using ECharts
            chart = ui.echart({
                'tooltip': {'trigger': 'item'},
                'series': [{
                    'type': 'venn',
                    'data': [
                        {'name': 'Economic', 'value': 10, 'itemStyle': {'color': '#3b82f6', 'opacity': 0.6}},
                        {'name': 'Social', 'value': 10, 'itemStyle': {'color': '#f59e0b', 'opacity': 0.6}},
                        {'name': 'Environmental', 'value': 10, 'itemStyle': {'color': '#10b981', 'opacity': 0.6}},
                        {'name': 'Equitable', 'sets': ['Social', 'Environmental'], 'value': 2},
                        {'name': 'Viable', 'sets': ['Economic', 'Environmental'], 'value': 2},
                        {'name': 'Bearable', 'sets': ['Economic', 'Social'], 'value': 2},
                        {'name': 'Sustainable', 'sets': ['Economic', 'Social', 'Environmental'], 'value': 1}
                    ]
                }]
            }).classes('w-full h-96')
            
            ui.markdown('''
            - **Economic**: Feasibility, profit, and financial growth.
            - **Social**: Equity, health, safety, and community impact.
            - **Environmental**: Resource conservation, pollution prevention, and biodiversity.
            
            **Intersections**:
            - *Viable*: Economic + Environmental
            - *Bearable*: Social + Environmental
            - *Equitable*: Economic + Social
            - **Sustainable**: The sweet spot where all three overlap.
            ''').classes('text-lg max-w-md')

def sustainability_theory_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Weak vs. Strong Sustainability').classes('text-h5 q-mb-md')
        ui.markdown('''
        This concept explores the degree of **substitutability** between different types of "capital."
        - **Weak Sustainability**: Assumes human-made capital (technology, infrastructure) can substitute for natural capital (ecosystems, clean air).
        - **Strong Sustainability**: Assumes natural capital is non-substitutable and must be preserved independently.
        ''')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-80'):
                ui.label('Investment vs. Extraction').classes('font-bold')
                investment = ui.slider(min=0, max=100, value=50).props('label-always')
                ui.label('Human Capital Investment (Growth):').bind_text_from(investment, 'value')
                
                extraction = ui.slider(min=0, max=100, value=30).props('label-always')
                ui.label('Natural Capital Extraction:').bind_text_from(extraction, 'value')
                
                theory_type = ui.radio(['Weak', 'Strong'], value='Weak').props('inline')
                ui.label('Sustainability Framework:').classes('text-xs text-gray-500')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'title': {'text': 'Capital Trend Over Time', 'left': 'center'},
                    'legend': {'bottom': 0},
                    'xAxis': {'type': 'category', 'data': [f'Year {i}' for i in range(11)]},
                    'yAxis': {'type': 'value', 'name': 'Capital Index'},
                    'series': [
                        {'name': 'Human Capital', 'type': 'line', 'data': [], 'smooth': True, 'lineStyle': {'color': '#3b82f6'}},
                        {'name': 'Natural Capital', 'type': 'line', 'data': [], 'smooth': True, 'lineStyle': {'color': '#10b981'}},
                        {'name': 'Total Sustainability', 'type': 'line', 'data': [], 'lineStyle': {'color': '#ef4444', 'width': 4}}
                    ]
                }).classes('w-full h-80')

                def update():
                    h_growth = investment.value / 1000
                    n_decay = extraction.value / 1000
                    
                    h_vals = [100 * (1 + h_growth)**i for i in range(11)]
                    n_vals = [100 * (1 - n_decay)**i for i in range(11)]
                    
                    if theory_type.value == 'Weak':
                        # Total = Sum of capitals
                        total_vals = [h + n for h, n in zip(h_vals, n_vals)]
                    else:
                        # Total = Min of the two (limiting factor is natural capital)
                        total_vals = [min(h, n) * 2 for h, n in zip(h_vals, n_vals)]
                    
                    chart.options['series'][0]['data'] = [round(v, 1) for v in h_vals]
                    chart.options['series'][1]['data'] = [round(v, 1) for v in n_vals]
                    chart.options['series'][2]['data'] = [round(v, 1) for v in total_vals]
                    chart.update()

                investment.on('update:model-value', update)
                extraction.on('update:model-value', update)
                theory_type.on('update:model-value', update)
                update()

def carbon_calculator_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Project Carbon Footprint Calculator').classes('text-h5 q-mb-md')
        ui.markdown('Estimate the embodied carbon of common civil engineering materials.')
        
        # Embodied carbon factors (kg CO2e per kg or m3) - Approximate values
        factors = {
            'Concrete (m3)': 250, # Average C25/30
            'Steel (tons)': 1850, # Recycled vs Virgin mix
            'Timber (m3)': -400,  # Negative due to sequestration
            'Asphalt (tons)': 60,
        }
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-80'):
                ui.label('Material Volumes').classes('font-bold')
                v_con = ui.number('Concrete (m³)', value=100, min=0)
                v_stl = ui.number('Steel (Tons)', value=10, min=0)
                v_tmb = ui.number('Timber (m³)', value=0, min=0)
                v_asp = ui.number('Asphalt (Tons)', value=0, min=0)
                
                ui.button('Calculate Impact', icon='eco', on_click=lambda: calculate()).classes('w-full q-mt-md')

            with ui.column().classes('flex-1 items-center justify-center'):
                impact_label = ui.label('0.0').classes('text-h2 font-black text-green-800')
                ui.label('Total metric tons of CO₂ equivalent').classes('text-lg text-gray-500 uppercase')
                
                chart = ui.echart({
                    'title': {'text': 'Impact Breakdown', 'left': 'center'},
                    'series': [{
                        'type': 'pie',
                        'radius': '60%',
                        'data': [],
                        'label': {'show': True, 'formatter': '{b}: {d}%'}
                    }]
                }).classes('w-full h-64')

        def calculate():
            c = v_con.value * factors['Concrete (m3)']
            s = v_stl.value * factors['Steel (tons)']
            t = v_tmb.value * factors['Timber (m3)']
            a = v_asp.value * factors['Asphalt (tons)']
            
            total_kg = c + s + t + a
            total_tons = total_kg / 1000
            
            impact_label.text = f'{total_tons:,.1f}'
            impact_label.classes('text-red-800' if total_tons > 100 else 'text-green-800', remove='text-red-800 text-green-800')
            
            chart.options['series'][0]['data'] = [
                {'name': 'Concrete', 'value': max(0, c)},
                {'name': 'Steel', 'value': max(0, s)},
                {'name': 'Timber', 'value': max(0, t)},
                {'name': 'Asphalt', 'value': max(0, a)},
            ]
            chart.update()

        calculate()
