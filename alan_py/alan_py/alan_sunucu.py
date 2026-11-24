import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea


class AlanSunucu(Node):
    def __init__(self):
        super().__init__('alan_sunucu')
        self.srv = self.create_service(
            RectangleArea,
            'rectangle_area',
            self.alan_hesapla_callback
        )
        self.get_logger().info('RectangleArea servisi hazir ve istek bekliyor...')

    def alan_hesapla_callback(self, request, response):
        if request.width < 0 or request.height < 0:
            response.area = 0.0
            response.success = False
            self.get_logger().warn(
                f'Gecersiz istek (negatif deger) -> width: {request.width}, height: {request.height} | success: False'
            )
        else:
            response.area = request.width * request.height
            response.success = True
            self.get_logger().info(
                f'Gelen istek -> width: {request.width}, height: {request.height} | Yanit -> area: {response.area}, success: True'
            )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = AlanSunucu()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()