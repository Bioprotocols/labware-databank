from sila2.client import SilaClient

client = SilaClient("127.0.0.1", 50052, insecure=True)

print(client.SiLAService.ImplementedFeatures.get())