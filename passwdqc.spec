#
# Conditional build:
%bcond_without	audit	# libaudit support in PAM (disable for use with PAM without audit support)

Summary:	A password/passphrase strength checking and policy enforcement toolset
Summary(pl.UTF-8):	Narzędzia do sprawdzania i wymuszania polityki jakości haseł
Name:		passwdqc
Version:	1.4.0
Release:	2
License:	BSD
Group:		Base
Source0:	https://www.openwall.com/passwdqc/%{name}-%{version}.tar.gz
# Source0-md5:	204de4ff2e95095272bba1b0cbab1579
URL:		https://www.openwall.com/passwdqc/
%{?with_audit:BuildRequires:	audit-libs-devel}
BuildRequires:	pam-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
passwdqc is a password/passphrase strength checking and policy
enforcement toolset, including a PAM module (pam_passwdqc),
command-line programs (pwqcheck and pwqgen), and a library
(libpasswdqc).

pwqcheck and pwqgen are standalone password/passphrase strength
checking and random passphrase generator programs, respectively, which
are usable from scripts.

libpasswdqc is the underlying library, which may also be used from
third-party programs.

%description -l pl.UTF-8
passwdqc to zbiór narzędzi do sprawdzania jakości haseł i wymuszania
jej polityki. Zawiera moduł PAM (pam_passwdqc), programy uruchamiane z
linii poleceń (pwqcheck i pwqgen) oraz bibliotekę (libpasswdqc).

pwqcheck oraz pwqgen to samodzielne programy do - odpowiednio -
sprawdzania jakości hasła oraz generowania losowych haseł, nadające
się do wykorzystania w skryptach.

libpasswdqc to będąca ich podstawą biblioteka, którą można
wykorzystywać także w innych programach.

%package devel
Summary:	Header files for building passwdqc-aware applications
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files needed for building
passwdqc-aware applications.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia aplikacji
wykorzystujących passwdqc.

%package -n pam-pam_passwdqc
Summary:	Password quality-control PAM module
Summary(pl.UTF-8):	Moduł PAM do sprawdzania jakości haseł
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description -n pam-pam_passwdqc
The pam_passwdqc module is a simple password strength checking module
for PAM, normally invoked on password changes by programs such as
passwd(1). In addition to checking regular passwords, it's capable of
enforcing a policy, and offering ramdomly-generated passphrases, with
all of these features being optional and easily (re)configurable.

%description -n pam-pam_passwdqc -l pl.UTF-8
Moduł pam_passwdc to prosty moduł PAM do sprawdzania jakości haseł,
zwykle wywoływany przy zmianie hasła przez programy takie jak
passwd(1). Poza sprawdzaniem zwykłych haseł, potrafi wymuszać ich
politykę i oferuje hasła losowo generowane. Wszystkie te elementy są
opcjonalne i łatwo (re)konfigurowalne.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -W -DLINUX_PAM %{?with_audit:-DHAVE_LIBAUDIT}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir} \
	SHARED_LIBDIR=/%{_lib} \
	DEVEL_LIBDIR=%{_libdir} \
	SECUREDIR=/%{_lib}/security

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README pwqcheck.php
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/passwdqc.conf
%attr(755,root,root) /%{_lib}/libpasswdqc.so.0
%attr(755,root,root) %{_bindir}/pwqcheck
%attr(755,root,root) %{_bindir}/pwqgen
%{_mandir}/man1/pwqcheck.1*
%{_mandir}/man1/pwqgen.1*
%{_mandir}/man5/passwdqc.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpasswdqc.so
%{_includedir}/passwdqc.h

%files -n pam-pam_passwdqc
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_passwdqc.so
%{_mandir}/man8/pam_passwdqc.8*
