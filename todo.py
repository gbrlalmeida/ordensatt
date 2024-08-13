import flet as ft
import psycopg2

class ToDo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_width = 375
        self.page.window_height = 667
        self.page.window_resizable = False
        self.page.bgcolor = ft.colors.WHITE
        self.page.title = 'Ordens'
        self.db_config = {}
        self.current_user = None
        self.main_page()

    def main_page(self):
        self.menu_open = False
        self.menu_button = ft.IconButton(
            icon=ft.icons.MENU,
            on_click=self.toggle_menu
        )

        add_order_item = ft.Row(
            controls=[
                ft.Icon(ft.icons.CONTENT_PASTE, size=24, color=ft.colors.BLUE_900),
                ft.TextButton(
                    text="Adicionar Ordem",
                    on_click=self.add_order,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_900
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4
        )

        report_item = ft.Row(
            controls=[
                ft.Icon(ft.icons.ANALYTICS, size=24, color=ft.colors.BLUE_900),
                ft.TextButton(
                    text="Análise",
                    on_click=self.generate_report,
                    style=ft.ButtonStyle(
                        color=ft.colors.BLUE_900
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4
        )

        menu_items_container = ft.Column(
            controls=[
                add_order_item,
                report_item
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True
        )

        self.menu_content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(height=20),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding(20, 0, 20, 0),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=menu_items_container,
                    alignment=ft.alignment.center,
                    expand=True
                ),
                ft.Container(expand=True),
                ft.Row(
                    controls=[
                        ft.Container(width=0, expand=True),
                        ft.ElevatedButton(
                            text="Sair",
                            on_click=self.logout,
                            bgcolor=ft.colors.RED,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        ),
                        ft.Container(width=0, expand=True)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=50
                ),
            ],
            alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
        )

        self.menu = ft.Container(
            content=self.menu_content,
            width=250,
            bgcolor=ft.colors.GREY_200,
            alignment=ft.alignment.top_center,
            visible=self.menu_open,
            border_radius=20,
            animate=ft.Animation(duration=300)
        )

        self.input_task = ft.TextField(hint_text='Digite o número da ordem', expand=True)
        self.input_task.on_change = self.search_task
        search_button = ft.IconButton(icon=ft.icons.SEARCH, on_click=self.search_task)

        input_bar = ft.Row(
            controls=[
                self.input_task,
                search_button
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text='Pendentes', content=self.create_task_list('Pendentes')),
                ft.Tab(text='Em andamento', content=self.create_task_list('Em andamento')),
                ft.Tab(text='Finalizados', content=self.create_task_list('Finalizados'))
            ]
        )

        content_area = ft.Column(
            controls=[input_bar, self.tabs],
            expand=True
        )

        main_layout = ft.Row(
            controls=[
                self.menu,
                ft.Column(
                    controls=[
                        self.menu_button,
                        content_area
                    ],
                    expand=True
                )
            ],
            expand=True
        )

        self.page.add(main_layout)

    def toggle_menu(self, e):
        self.menu_open = not self.menu_open
        self.menu.visible = self.menu_open
        self.page.update()

    def search_task(self, e):
        search_value = self.input_task.value.strip()
        if search_value:
            search_results = self.get_order_by_id(search_value)
            if search_results:
                self.tabs.tabs[0].content.controls = [
                    self.create_task_button(search_results[0])
                ]
            else:
                self.tabs.tabs[0].content.controls = [
                    ft.Text(f"Nenhuma ordem encontrada com id: {search_value}", color=ft.colors.RED)
                ]
        else:
            self.tabs.tabs[0].content.controls = self.create_task_list('Pendentes').controls
        self.page.update()

    def create_task_list(self, status):
        orders = self.get_orders_by_status(status)
        return ft.Column(
            controls=[
                self.create_task_button(order[0]) for order in orders
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=10
        )

    def create_task_button(self, order_id):
        return ft.ElevatedButton(
            text=f"Ordem {order_id}",
            on_click=self.view_order_details,
            expand=True
        )

    def get_orders_by_status(self, status):
        # Placeholder for database interaction
        return []

    def get_order_by_id(self, order_id):
        # Placeholder for database interaction
        return []

    def view_order_details(self, e):
        print("Ordem detalhada")

    def add_order(self, e):
        print("Adicionar Ordem")

    def generate_report(self, e):
        self.show_analysis_page()

    def show_analysis_page(self):
        pending_orders = len(self.get_orders_by_status('Pendente'))
        ongoing_orders = len(self.get_orders_by_status('Em andamento'))
        completed_orders = len(self.get_orders_by_status('Finalizado'))

        async def on_chart_event(e: ft.PieChartEvent):
            for idx, section in enumerate(chart.sections):
                if idx == e.section_index:
                    section.radius = hover_radius
                    section.title_style = hover_title_style
                else:
                    section.radius = normal_radius
                    section.title_style = normal_title_style
            await chart.update_async()

        normal_radius = 50
        hover_radius = 60
        normal_title_style = ft.TextStyle(
            size=16, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )
        hover_title_style = ft.TextStyle(
            size=22,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )

        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    40,
                    title="40%",
                    title_style=normal_title_style,
                    color=ft.colors.BLUE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    30,
                    title="30%",
                    title_style=normal_title_style,
                    color=ft.colors.YELLOW,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.colors.PURPLE,
                    radius=normal_radius,
                ),
                ft.PieChartSection(
                    15,
                    title="15%",
                    title_style=normal_title_style,
                    color=ft.colors.GREEN,
                    radius=normal_radius,
                ),
            ],
            sections_space=0,
            center_space_radius=40,
            on_chart_event=on_chart_event,
            expand=True,
        )

        analysis_page = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            icon_size=30,
                            on_click=self.go_back_to_main_page
                        ),
                        ft.Text("Análises", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    height=50,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Ordens Pendentes", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                    ft.Text(f"{pending_orders}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            ),
                            ft.Container(
                                content=chart,
                                height=200,  # Adjust the height as needed
                                padding=ft.Padding(20, 0, 20, 0),
                                alignment=ft.alignment.center
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Ordens em Andamento", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                    ft.Text(f"{ongoing_orders}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Ordens Finalizadas", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                    ft.Text(f"{completed_orders}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            ),

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    ),
                    padding=ft.Padding(20, 20, 20, 20),
                    alignment=ft.alignment.center
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        self.page.controls.clear()
        self.page.add(analysis_page)
        self.page.update()

    def go_back_to_main_page(self, e):
        self.page.controls.clear()
        self.main_page()

    def logout(self, e):
        self.page.remove(self.page.controls[0])
        self.main_page()

def main(page: ft.Page):
    ToDo(page)

ft.app(target=main)

