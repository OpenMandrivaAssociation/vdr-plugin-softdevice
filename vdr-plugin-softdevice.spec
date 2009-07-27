
%define plugin	softdevice
%define name	vdr-plugin-%plugin
%define version	0.5.0
%define snapshot 20090321
%define rel	2
%if %snapshot
%define release	%mkrel 5.%snapshot.%rel
%else
%define release	%mkrel %rel
%endif

Summary:	VDR plugin: A software emulated MPEG2 device
Name:		%name
Version:	%version
Release:	%release
Group:		Video
License:	GPLv2+
URL:		http://softdevice.berlios.de/
%if %snapshot
Source:		vdr-%plugin-%snapshot.tar.bz2
%else
Source:		http://download.berlios.de/softdevice/vdr-%plugin-%version.tgz
%endif
Patch0:		softdevice-linking-order.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	vdr-abi = %vdr_abi
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	ffmpeg-devel
BuildRequires:	libalsa-devel
%if %mdkversion >= 200700
BuildRequires:	dfb++-devel
BuildRequires:	libxv-devel
BuildRequires:	libxinerama-devel
BuildRequires:	dos2unix
%else
BuildRequires:	X11-devel
%endif
Requires(post):	vdr-common

%description
This plugin is a MPEG2 decoder. It can be used as an output device
for the vdr. Possible output devices are Xv, DirectFB, Vidix or a
framebuffer.

%prep
%if %snapshot
%setup -q -n %plugin
%else
%setup -q -n %plugin-%version
%endif
%patch0 -p0
dos2unix CHANGELOG
%vdr_plugin_prep

%vdr_plugin_params_begin %plugin
# See plugin documentation and 'vdr --help' for detailed info
#
# audio output plugin and options
# example: "alsa:mixer"
var=AUDIO_OUT
param='-ao AUDIO_OUT'
# video output plugin and options
# example: "xv:full"
var=VIDEO_OUT
param='-vo VIDEO_OUT'
%vdr_plugin_params_end

%build
# simple configure script
./configure --disable-subplugins --enable-yaepg
%vdr_plugin_build

%install
rm -rf %{buildroot}
%vdr_plugin_install
install -d -m755 %{buildroot}%{_bindir}
install -m755 ShmClient %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%post
%{_bindir}/gpasswd -a vdr audio >/dev/null
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY CHANGELOG
%{_bindir}/ShmClient
