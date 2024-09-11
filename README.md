<h1>Aplicativo de Monitoramento de Vibração</h1>
<a href='https://drive.google.com/file/d/1CvkLxWJfazfs5merxKb_dxoQEUrOrzzj/view?usp=drive_link'>Baixe o .EXE aqui.</a>
<br>
Para rodar este app em seu ambiente siga os passos abaixo.

Instale a versão do python que foi utilizada no projeto.
```
python3.11
```
Crie um ambiente virtual em python
```
python3.11 -m venv .venv
```
Ative o ambiente.
```
CMD: .\.venv\Scripts\activate
Linux: source .venv/bin/activate
```
Após ativar seu ambiente instale as dependencias requeridas.
```
pip install -r requirements.txt
```
Execute.
```
flet run
```

<h1>Funcionalidade do Aplicativo</h1>

<p>Cadastre seu servidor MQTT</p>
<image src="https://github.com/user-attachments/assets/d64c5552-ad80-4d2a-8c12-ebee3e48bff0">

<p>Cadastre seu topico de leitura</p>
<image src="https://github.com/user-attachments/assets/4822bc59-6ed5-4ab4-adea-82d2c7936a90">

O aplicativo espera o json dessa forma:
```json
{
  "y": 23,
  "x": 21,
  "z": 13,
  "timestamp": 17273274
}
```
<p>Selecione seu equipamento:</p>
<image src="https://github.com/user-attachments/assets/50bab35f-2957-4161-b666-fecba5a88bc6">

<p>Suas informações irão aparecer na tabela</p>
<image src="https://github.com/user-attachments/assets/95dc3bd3-8ce0-4d40-85a0-6a7a6a09aa74">
<p>A tabela não atualiza em tempo real, é necessario selecionar novamente para atualizar</p>
