import sys
import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea


class AlanIstemci(Node):
    def __init__(self):
        super().__init__('alan_istemci')
        self.cli = self.create_client(RectangleArea, 'rectangle_area')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Servis bekleniyor...')

    def istek_gonder(self, width, height):
        req = RectangleArea.Request()
        req.width = float(width)
        req.height = float(height)
        return self.cli.call_async(req)


def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) < 3:
        print('Kullanim: ros2 run alan_py alan_istemci <width> <height>')
        rclpy.shutdown()
        return

    node = AlanIstemci()
    future = node.istek_gonder(sys.argv[1], sys.argv[2])
    rclpy.spin_until_future_complete(node, future)

    response = future.result()
    if response.success:
        node.get_logger().info(
            f'Sonuc: width={sys.argv[1]}, height={sys.argv[2]} -> area={response.area}, success={response.success}'
        )
    else:
        node.get_logger().warn(
            f'Istek reddedildi! Negatif deger girilemez (width={sys.argv[1]}, height={sys.argv[2]}) -> success={response.success}'
        )

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()