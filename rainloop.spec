Name:           rainloop
Version:        1.12.1
Release:        1%{?dist}
Summary:        Simple, modern & fast web-based email client.
License:        AGPLv3+
Group:          Networking/WWW
URL:            http://rainloop.net
Source0:        https://github.com/Rainloop/rainloop-webmail/releases/download/v%{version}/%{name}-community-%{version}.zip
Requires:       httpd
Requires:	    php
Requires:       php-mysql
Requires:       php-ldap
BuildArch:      noarch

%description
RainLoop Webmail
Simple, modern & fast web-based email client. Modest system requirements, decent performance, 
simple installation and upgrade, no database required - 
all these make RainLoop Webmail a perfect choice for your email solution.


%prep
mkdir %{name}-%{version}
cd %{name}-%{version}
unzip %{SOURCE0}

%build
# Nothing to do!!

%install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -r %{name}-%{version}/* %{buildroot}%{_datadir}/%{name}

# apache configuration
install -d -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf<<EOF
# rainloop configuration

Alias /%{name} %{_datadir}/%{name}

# Redirect to https
RewriteEngine On
RewriteRule ^/%{name}(/.*)?$  https://%{HTTP_HOST}/%{name}$1  [L,R=301]

<Directory %{_datadir}/%{name}>
    Require all granted
    php_admin_value post_max_size 25M
    php_admin_value upload_max_filesize 25M
</Directory>
<Directory %{_datadir}/%{name}/data>
    Require all denied
</Directory>
EOF

%files
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%dir %attr(0750,apache,apache) %{_datadir}/%{name}/data

%post
/sbin/service httpd condrestart > /dev/null 2>&1 || :
%postun
/sbin/service httpd condrestart > /dev/null 2>&1 || :

%changelog
* Sun Sep 02 2018 stephane de labrusse <stephdl@de-labrusse.fr> 1.12.1-el7
- upstream upgrade

* Thu May 10 2018 stephane de Labrusse <stephdl@de-labrusse.fr> 1.12.0-el7
- First release of rainloop
