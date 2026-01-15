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
        t4 = ui.tab('IRR Visualizer')
        t5 = ui.tab('Depreciation')
        t6 = ui.tab('Loan Amortization')
        t7 = ui.tab('Incremental IRR')

    with ui.tab_panels(tabs, value=t1).classes('w-full bg-transparent'):
        with ui.tab_panel(t1):
            single_payment_calculator()
        with ui.tab_panel(t2):
            uniform_series_calculator()
        with ui.tab_panel(t3):
            project_comparison_module()
        with ui.tab_panel(t4):
            irr_visualizer_tool()
        with ui.tab_panel(t5):
            depreciation_tool()
        with ui.tab_panel(t6):
            loan_amortization_tool()
        with ui.tab_panel(t7):
            incremental_irr_tool()

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
                    
                    current_data = [p * ((1 + i)**year) for year in range(int(n) + 1)]
                    chart.options['series'][0]['data'] = current_data
                    chart.update()

                def save_scenario():
                    p = p_slider.value
                    i = rate_slider.value / 100
                    n = years_slider.value
                    saved_data = [p * ((1 + i)**year) for year in range(int(n) + 1)]
                    chart.options['series'][1]['data'] = saved_data
                    chart.options['series'][1]['name'] = f'Saved (i={rate_slider.value}%)'
                    chart.update()
                    ui.notify('Scenario Saved for Comparison!')

                p_slider.on('update:model-value', update)
                rate_slider.on('update:model-value', update)
                years_slider.on('update:model-value', update)
                
                ui.button('Save Current as Base', icon='save', on_click=save_scenario).classes('w-full q-mt-md').props('outline')

        chart = ui.echart({
            'xAxis': {'type': 'category', 'data': [str(y) for y in range(31)], 'name': 'Year'},
            'yAxis': {'type': 'value', 'name': 'Value ($)'},
            'legend': {'bottom': 0},
            'tooltip': {'trigger': 'axis'},
            'series': [
                {
                    'name': 'Current',
                    'data': [],
                    'type': 'line',
                    'smooth': True,
                    'areaStyle': {'color': 'rgba(59, 130, 246, 0.2)'},
                    'lineStyle': {'color': '#3b82f6', 'width': 3}
                },
                {
                    'name': 'Saved Scenario',
                    'data': [],
                    'type': 'line',
                    'smooth': True,
                    'lineStyle': {'color': '#94a3b8', 'width': 2, 'type': 'dashed'}
                }
            ]
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

        with ui.row().classes('w-full gap-4 q-mt-md items-center'):
            inflation = ui.slider(min=0, max=10, value=0, step=0.1).classes('flex-1')
            ui.label('Inflation:').bind_text_from(inflation, 'value', backward=lambda v: f'Inflation: {v}%')
            ui.icon('info', size='1rem').tooltip('Adjusts discount rate to "Real" rate: i_real = (i - f)/(1 + f)')

        def calculate_pw():
            i_nom = rate.value / 100
            f = inflation.value / 100
            # Fisher relation: (1+i_nom) = (1+i_real)(1+f) -> i_real = (1+i_nom)/(1+f) - 1
            i = (1 + i_nom) / (1 + f) - 1
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

def irr_visualizer_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Internal Rate of Return (IRR) Visualizer').classes('text-h5 q-mb-md')
        ui.markdown('''
        The **IRR** is the discount rate that makes the **Net Present Value (NPV)** of all cash flows equal to zero. 
        It is the "breakeven" interest rate for an investment.
        ''')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-64'):
                ui.label('Cash Flow Parameters').classes('font-bold')
                initial_cost = ui.number('Initial Investment ($)', value=10000, min=0)
                annual_benefit = ui.number('Annual Benefit ($)', value=2500, min=0)
                life_span = ui.number('Life (Years)', value=8, min=1, precision=0)
                
                ui.button('Calculate IRR', icon='calculate', on_click=lambda: update()).classes('w-full q-mt-md')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'title': {'text': 'NPV vs. Interest Rate', 'left': 'center'},
                    'xAxis': {'type': 'value', 'name': 'Interest Rate (%)', 'nameLocation': 'middle', 'nameGap': 25},
                    'yAxis': {'type': 'value', 'name': 'Net Present Value (NPV)'},
                    'series': [
                        {
                            'name': 'NPV Curve',
                            'type': 'line',
                            'data': [],
                            'smooth': True,
                            'lineStyle': {'color': '#3b82f6', 'width': 3},
                        },
                        {
                            'name': 'X-Axis (Zero NPV)',
                            'type': 'line',
                            'data': [[0, 0], [50, 0]],
                            'lineStyle': {'color': '#000', 'type': 'dashed', 'width': 1},
                            'symbol': 'none'
                        }
                    ],
                    'tooltip': {'trigger': 'axis', 'formatter': 'Rate: {b}% <br/> NPV: ${c}'}
                }).classes('w-full h-80')
                
                res_box = ui.row().classes('w-full justify-center q-mt-md p-4 bg-blue-50 rounded border')
                with res_box:
                    ui.label('Calculated IRR:').classes('text-lg')
                    irr_label = ui.label('- %').classes('text-h6 font-black text-blue-800')

        def update():
            c0 = initial_cost.value
            a = annual_benefit.value
            n = int(life_span.value)
            
            rates = np.linspace(0.01, 0.5, 50) # 1% to 50%
            npv_data = []
            
            for r in rates:
                factor = ((1 + r)**n - 1) / (r * (1 + r)**n)
                npv = -c0 + a * factor
                npv_data.append([round(r*100, 2), round(npv, 2)])
            
            chart.options['series'][0]['data'] = npv_data
            chart.update()
            
            # Binary search for IRR
            low, high = 0.0001, 1.0
            for _ in range(20):
                mid = (low + high) / 2
                f = ((1+mid)**n - 1) / (mid * (1+mid)**n)
                if -c0 + a*f > 0: low = mid
                else: high = mid
            
            irr_label.text = f'{low*100:.2f}%'

        update()

def depreciation_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Depreciation Methods: SL, SYD, DB, & MACRS').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-4'):
            cost = ui.number('Initial Cost ($)', value=10000, min=0).classes('w-32')
            salvage = ui.number('Salvage ($)', value=1000, min=0).classes('w-32')
            life = ui.select([3, 5, 7, 10], value=5, label='Life (Years)').classes('w-32')
            
            ui.button('Compare', on_click=lambda: update()).classes('q-mb-sm')

        chart = ui.echart({
            'title': {'text': 'Annual Depreciation Expense', 'left': 'center'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'bottom': 0},
            'xAxis': {'type': 'category', 'data': []},
            'yAxis': {'type': 'value', 'name': 'Expense ($)'},
            'series': [
                {'name': 'Straight Line (SL)', 'type': 'bar', 'data': []},
                {'name': 'SYD', 'type': 'bar', 'data': []},
                {'name': 'MACRS (GDS)', 'type': 'bar', 'data': []}
            ]
        }).classes('w-full h-80 q-mt-md')

        def update():
            c = cost.value
            s = salvage.value
            n = int(life.value)
            
            # SL
            sl = [(c - s) / n] * n
            
            # SYD
            syd_sum = n * (n + 1) / 2
            syd = [(n - y + 1) / syd_sum * (c - s) for y in range(1, n + 1)]
            
            # MACRS
            macrs_pcts = {
                3: [33.33, 44.45, 14.81, 7.41],
                5: [20.00, 32.00, 19.20, 11.52, 11.52, 5.76],
                7: [14.29, 24.49, 17.49, 12.49, 8.93, 8.92, 8.93, 4.46],
                10: [10.00, 18.00, 14.40, 11.52, 9.22, 7.37, 6.55, 6.55, 6.56, 6.55, 3.28]
            }
            m = [round(c * (p/100), 2) for p in macrs_pcts[n]]
            
            # Sync x-axis
            max_len = max(n, len(m))
            chart.options['xAxis']['data'] = [f'Yr {i}' for i in range(1, max_len + 1)]
            chart.options['series'][0]['data'] = [round(v, 2) for v in sl + [0]*(max_len-n)]
            chart.options['series'][1]['data'] = [round(v, 2) for v in syd + [0]*(max_len-n)]
            chart.options['series'][2]['data'] = m
            chart.update()

        update()

def loan_amortization_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Loan Amortization Schedule').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('w-64'):
                principal = ui.number('Loan Amount ($)', value=200000, min=0)
                rate_ui = ui.number('Annual Interest (%)', value=5, format='%.2f')
                years_ui = ui.number('Term (Years)', value=30, precision=0)
                
                ui.button('Generate Table', icon='table_view', on_click=lambda: update_table()).classes('w-full q-mt-md')

            with ui.column().classes('flex-1'):
                chart = ui.echart({
                    'title': {'text': 'Principal vs. Interest Over Time', 'left': 'center'},
                    'tooltip': {'trigger': 'axis'},
                    'legend': {'bottom': 0},
                    'xAxis': {'type': 'category', 'data': []},
                    'yAxis': {'type': 'value', 'name': 'Payment Component ($)'},
                    'series': [
                        {'name': 'Principal', 'type': 'bar', 'stack': 'total', 'data': [], 'itemStyle': {'color': '#3b82f6'}},
                        {'name': 'Interest', 'type': 'bar', 'stack': 'total', 'data': [], 'itemStyle': {'color': '#f59e0b'}}
                    ]
                }).classes('w-full h-80')

        def update_table():
            p = principal.value
            r = (rate_ui.value / 100) / 12 # Monthly
            n = int(years_ui.value) * 12 # Monthly periods
            
            if r == 0:
                payment = p / n
            else:
                payment = p * (r * (1 + r)**n) / ((1 + r)**n - 1)
            
            p_comp = []
            i_comp = []
            balance = p
            
            # Record yearly totals to keep chart readable
            for year in range(1, int(years_ui.value) + 1):
                y_p = 0
                y_i = 0
                for _ in range(12):
                    interest = balance * r
                    prin = payment - interest
                    y_p += prin
                    y_i += interest
                    balance -= prin
                p_comp.append(round(y_p, 2))
                i_comp.append(round(y_i, 2))
            
            chart.options['xAxis']['data'] = [f'Yr {i}' for i in range(1, int(years_ui.value) + 1)]
            chart.options['series'][0]['data'] = p_comp
            chart.options['series'][1]['data'] = i_comp
            chart.update()

        update_table()

def incremental_irr_tool():
    with ui.card().classes('w-full p-6 shadow-lg'):
        ui.label('Incremental IRR Analysis').classes('text-h5 q-mb-md')
        ui.markdown('''
        Used to determine if the **additional investment** in a more expensive project is justified.
        We calculate the IRR of the *difference* in cash flows ($\Delta CF = CF_B - CF_A$).
        ''')
        
        with ui.row().classes('w-full gap-8'):
            with ui.column().classes('flex-1 p-4 bg-gray-50 rounded'):
                ui.label('Project A (Lower Cost)').classes('font-bold border-b w-full mb-2')
                c_a = ui.number('Cost ($)', value=5000)
                b_a = ui.number('Annual Benefit ($)', value=1500)
            
            with ui.column().classes('flex-1 p-4 bg-gray-50 rounded'):
                ui.label('Project B (Higher Cost)').classes('font-bold border-b w-full mb-2')
                c_b = ui.number('Cost ($)', value=8000)
                b_b = ui.number('Annual Benefit ($)', value=2200)
        
        n_ui = ui.number('Shared Life (Years)', value=10, classes='w-full q-mt-md')
        ui.button('Determine Incremental IRR', icon='trending_up', on_click=lambda: calculate()).classes('w-full q-mt-md')
        
        res_label = ui.label('').classes('text-xl font-bold text-center w-full q-mt-md text-blue-800')

        def calculate():
            dc0 = c_b.value - c_a.value
            da = b_b.value - b_a.value
            n = int(n_ui.value)
            
            if dc0 <= 0 or da <= 0:
                res_label.text = "Incremental cost or benefit must be positive for IRR calculation."
                return

            # Solve for r: -dc0 + da * factor = 0
            # factor = ((1+r)**n - 1) / (r * (1+r)**n)
            low, high = 0.0001, 1.0
            for _ in range(20):
                mid = (low + high) / 2
                f = ((1+mid)**n - 1) / (mid * (1+mid)**n)
                if -dc0 + da*f > 0: low = mid
                else: high = mid
            
            irr = low * 100
            res_label.text = f'Incremental IRR (ΔB/ΔC): {irr:.2f}%'
            ui.notify(f'If MARR < {irr:.1f}%, choose Project B.')
