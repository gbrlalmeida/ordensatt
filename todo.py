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
        self.db_config = {
            'dbname': 'servicos',
            'user': 'GABRIEL',
            'password': '123456',
            'host': '192.168.10.52',
            'port': '5432'
        }
        self.current_user = None
        self.show_login_page()

    def show_login_page(self):
        logo = ft.Image(src="img/grupoatt-1-Photoroom.png", width=170, height=170)

        self.username = ft.TextField(
            label="Usuário", 
            width=300,
            color=ft.colors.BLACK,
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
        )
        self.password = ft.TextField(
            label="Senha", 
            width=300, 
            password=True, 
            can_reveal_password=True,
            color=ft.colors.BLACK,
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
        )
        login_button = ft.ElevatedButton(
            text="Login", 
            on_click=self.login,
            style=ft.ButtonStyle(
                elevation=2
            )
        )

        self.error_message = ft.Text("", color=ft.colors.RED)

        login_form = ft.Column(
            controls=[
                logo,
                self.username,
                self.password,
                login_button,
                self.error_message,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        centered_container = ft.Container(
            content=login_form,
            alignment=ft.alignment.center,
            expand=True,
        )

        self.page.add(centered_container)
        self.login_form = centered_container

    def login(self, e):
        user = self.authenticate_user(self.username.value, self.password.value)
        if user:
            self.current_user = user[0]
            self.page.remove(self.login_form)
            self.main_page()
        else:
            self.error_message.value = "Usuário ou senha inválidos"
            self.password.value = ""
            self.page.update()

    def authenticate_user(self, username, password):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s AND senha = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

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
            alignment=ft.MainAxisAlignment.START,
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
            alignment=ft.MainAxisAlignment.START,
            spacing=4
        )

        # Container for menu items with centered alignment
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

        # Centering menu content
        self.menu_content = ft.Column(
            controls=[
                # Container for the logo, username, and back arrow
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(width=0, expand=True),
                                        ft.IconButton(
                                            icon=ft.icons.ARROW_BACK,
                                            on_click=self.toggle_menu,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                                bgcolor=ft.colors.TRANSPARENT,
                                                color=ft.colors.BLACK
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                                padding=ft.Padding(10, 10, 10, 10),
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.CircleAvatar(
                                            content=ft.Image(src="img/foto_usuario.png", fit=ft.ImageFit.COVER),
                                            radius=30,
                                        ),
                                        ft.Text(
                                            self.current_user,
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.BLACK
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                padding=ft.Padding(20, 0, 20, 0),
                                alignment=ft.alignment.center
                            ),
                            ft.Container(height=20),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding(20, 0, 20, 0),
                    alignment=ft.alignment.center,
                ),
                # Menu items container
                ft.Container(
                    content=menu_items_container,
                    alignment=ft.alignment.center,
                    expand=True
                ),
                # Spacer to push the "Logout" button to the bottom
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
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT id_ordem FROM ordens WHERE status = %s", (status,))
            orders = cursor.fetchall()
            cursor.close()
            conn.close()
            return orders
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return []

    def get_order_by_id(self, order_id):
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ordens WHERE id_ordem = %s", (order_id,))
            order = cursor.fetchall()
            cursor.close()
            conn.close()
            return order
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
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

        analysis_page = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Dash", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        ft.Text("Ordens", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("Número de ordens pendentes", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                    ft.Text(f"{pending_orders}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Número de ordens em andamento", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                    ft.Text(f"{ongoing_orders}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=10
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text("Número de ordens finalizadas", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
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
                ft.ElevatedButton(text="Voltar", on_click=self.go_back_to_main_page)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

        # Remove the main page content
        self.page.controls.clear()
        
        # Add the analysis page content
        self.page.add(analysis_page)
        self.page.update()

    def go_back_to_main_page(self, e):
        self.page.controls.clear()
        self.main_page()

    def logout(self, e):
        self.page.remove(self.page.controls[0])
        self.show_login_page()

def main(page: ft.Page):
    ToDo(page)

ft.app(target=main)
