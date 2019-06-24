%define version 0.3.0
%define commit af3b7349b322169f5e57ce30da760e50d94644cc
Name: nvidia-xrun
# A git hash used in the version should start with "g" and then
# proceed with the first 7 characters of the commit message.
Version: %{version}+79
Release: 1%{?dist}
Summary: Utility to run separate X with discrete nvidia graphics with full performance.
License: GNU GPLv2
buildroot: %{_tmppath}/%{name}-root
BuildArch: noarch
Conflicts: nvidia-xrun-pm
# This forces the remote source code to be downloaded during the rpmbuild.
# It is ignored on Fedora COPR. A source RPM must be built elsewhere
# before being uploaded to be built as a binary RPM.
%undefine _disable_source_fetch
Source0: https://github.com/Witko/nvidia-xrun/archive/%{commit}.tar.gz
# The "systemd" package is required for the "_unitdir" macro.
BuildRequires: systemd

%description
This fork provides the benefits of nvidia-xrun without the extra dependency of bumblebee for power management. These utility scripts aim to make the life easier for nvidia cards users. It started with a revelation that bumblebee in current state offers very poor performance. This solution offers a bit more complicated procedure but offers a full GPU utilization.

%prep
# Extract the source tarball to ~/rpmbuild/BUILD/.
tar -x -v -f %{SOURCE0}

%install
mkdir -p %{buildroot}/%{_bindir}
install -pm 755 %{_builddir}/nvidia-xrun-%{commit}/nvidia-xrun %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_sysconfdir}/X11/xinit/
install -pm 644 %{_builddir}/nvidia-xrun-%{commit}/nvidia-xorg.conf %{buildroot}/%{_sysconfdir}/X11/
install -pm 755 %{_builddir}/nvidia-xrun-%{commit}/nvidia-xinitrc %{buildroot}/%{_sysconfdir}/X11/xinit/
mkdir -p %{buildroot}/%{_sysconfdir}/default
install -pm 644 %{_builddir}/nvidia-xrun-%{commit}/config/nvidia-xrun %{buildroot}/%{_sysconfdir}/default/
mkdir -p %{buildroot}/%{_unitdir}/
install -pm 644 %{_builddir}/nvidia-xrun-%{commit}/nvidia-xrun-pm.service %{buildroot}/%{_unitdir}/

%files
%{_bindir}/nvidia-xrun
%{_sysconfdir}/X11/nvidia-xorg.conf
%{_sysconfdir}/X11/xinit/nvidia-xinitrc
%{_sysconfdir}/default/nvidia-xrun
%{_unitdir}/nvidia-xrun-pm.service

%changelog
* Mon Jun 24 2019 Luke Short <ekultails@gmail.com> 0.3.0+79-1
- Switch to using the standardized GitVersion guidelines for the RPM version
- Update to the latest commit (af3b7349)

* Sun May 05 2019 Luke Short <ekultails@gmail.com> 0.3.0_g755d612-1
- Use commit hash for the source
- Update to the latest commit

* Thu Dec 28 2017 Abhiram Kuchibhotla <mailto:7677954+AxelSilverdew@users.noreply.github.com> 1
- Initial RPM spec release
