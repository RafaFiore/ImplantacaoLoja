<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://git.hostgator.com.br/especialistas/loja-implantacao">
    <img src="images/snappy_logo.jpg" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Implatanção Loja Hostgator</h3>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Sumário</summary>
  <ol>
    <li>
      <a href="#sobre-o-projeto">Sobre o Projeto</a>
      <ul>
        <li><a href="#linguagem">Linguagem</a></li>
      </ul>
    </li>
    <li>
      <a href="#pré-requisitos">Pré-requisitos</a>
    </li>
    <li><a href="#libs-do-python">Libs do Python</a></li>
    <li><a href="#utilização">Utilização</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contatos">Contatos</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Sobre o projeto

O projeto tem como objetivo automatizar a primeira etapa do serviço de implantações de Lojas.
Os pedidos recebidos da RD são tratados e encaminhados para os respectivos clientes, solicitando-os o preenchimento de um formulário.
Assim que o cliente responde o formulário, a solicitação é redirecionado ao time de Consultoria da Loja Hostgator.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Linguagem

* [![Python][Python.org]][Python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Pré-requisitos

* python 3.6+
* MySQL 5.6+

### Libs do Python

* requests
* mysql-python-connector
* fire
* pymsteams
* python-dotenv
* html-to-json

## Instalação
**OBS:** Caso o servidor ou sua máquina local já tenha instalado o Python e MySQL, pular para o passo 4.

1. **Atualizar o ambiente**

   ```sh
   yum update -y
   ```
2. **Instalar o MySQL**

   ```sh
   curl -sSLO https://dev.mysql.com/get/mysql80-community-release-el7-5.noarch.rpm
   ```
   ```sh
   sudo rpm -ivh mysql57-community-release-el7-9.noarch.rpm
   ```
   ```sh
   sudo yum install mysql-server
   ```
   ```sh
   sudo grep 'temporary password' /var/log/mysqld.log
   ```
   ```sh
   sudo mysql_secure_installation
   ```
3. **Instalar o Python 3**

   ```sh
   yum install -y python3
   ```
4. **nstalar as libs do Python**

   ```sh
   pip install requests
   ```
   ```sh
   pip install mysql-python-connector
   ```
   ```sh
   pip install fire
   ```
   ```sh
   pip install pymsteams
   ```
   ```sh
   pip install python-dotenv
   ```
   ```sh
   pip install html-to-json
   ```
5. **Clonar o repo**

   ```sh
   git clone git@git.hostgator.com.br:especialistas/loja-implantacao.git
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Utilização
* **Função principal**

   ```sh
   python3 Implantacao.py proccess_implatancao
   ```
* **Função de processamento de respostas do forms**

   ```sh
   python3 Implantacao.py process_form_answers
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Função para criar o schema
    - [ ] Função que verifica antes se já não existe o schema criado


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contatos

Rafael Fiorentini - rafael.fiorentini@newfold.com

#### Suplentes

Moises Junior - moises.junior@newfold.com

#### Supervisão

Larissa Vasconcelos - larissa.vasconcellos@newfold.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/